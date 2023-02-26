#!/bin/bash

# shellcheck disable=SC2046
workDir=$(realpath -- $(dirname "$0"))
dataDir="${workDir}/data/"
pythoncmd="python3"

[ -x "/usr/bin/python" ] && pythoncmd="python"
[ -x "/usr/bin/python3" ] && pythoncmd="python3"

#echo "${pythoncmd}"


# 全局变量
fundListPython="${workDir}/bin/get-all-fund.py"
fundInfoPython="${workDir}/bin/fund-name-by-code.py"
fundWorthPython="${workDir}/bin/fund-net-worth.py"

fundListFile="${dataDir}/fund-list.csv"


# 全局变量结束

function parseopts()
{
    local opt= optarg= i= shortopts=$1
    local -a longopts=() unused_argv=()

    shift
    while [[ $1 && $1 != '--' ]]; do
        longopts+=("$1")
        shift
    done
    shift

    longoptmatch() {
        local o longmatch=()
        for o in "${longopts[@]}"; do
            if [[ ${o%:} = "$1" ]]; then
                longmatch=("$o")
                break
            fi
            [[ ${o%:} = "$1"* ]] && longmatch+=("$o")
        done

        case ${#longmatch[*]} in
            1)
                opt=${longmatch%:}
                if [[ $longmatch = *: ]]; then
                    return 1
                else
                    return 0
                fi ;;
            0)
                return 255 ;;
            *)
                return 254 ;;
        esac
    }
    while (( $# )); do
        case $1 in
            --) # explicit end of options
                shift
                break
                ;;
            -[!-]*) # short option
                for (( i = 1; i < ${#1}; i++ )); do
                    opt=${1:i:1}

                    # option doesn't exist
                    if [[ $shortopts != *$opt* ]]; then
                        OPTRET=(--)
                        return 1
                    fi

                    OPTRET+=("-$opt")
                    # option requires optarg
                    if [[ $shortopts = *$opt:* ]]; then
                        if (( i < ${#1} - 1 )); then
                            OPTRET+=("${1:i+1}")
                            break
                        elif (( i == ${#1} - 1 )) && [[ "$2" ]]; then
                            OPTRET+=("$2")
                            shift
                            break
                        # parse failure
                        else
                            OPTRET=(--)
                            return 1
                        fi
                    fi
                done
                ;;
            --?*=*|--?*) # long option
                IFS='=' read -r opt optarg <<< "${1#--}"
                longoptmatch "$opt"
                case $? in
                    0)
                        if [[ $optarg ]]; then
                            OPTRET=(--)
                            return 1
                        else
                            OPTRET+=("--$opt")
                        fi
                        ;;
                    1)
                        if [[ $optarg ]]; then
                            OPTRET+=("--$opt" "$optarg")
                        elif [[ "$2" ]]; then
                            OPTRET+=("--$opt" "$2" )
                            shift
                        else
                            printf "%s: 配置选项 '--%s' 需要参数!\n" "${0##*/}" "$opt"
                            OPTRET=(--)
                            return 1
                        fi
                        ;;
                    254)
                        OPTRET=(--)
                        return 1
                        ;;
                    255)
                        # parse failure
                        printf "%s: 未定义的配置选项 '%s'\n" "${0##*/}" "--$opt"
                        OPTRET=(--)
                        return 1
                        ;;
                esac
                ;;
            *) # non-option arg encountered, add it as a parameter
                unused_argv+=("$1")
                ;;
        esac
        shift
    done
    # add end-of-opt terminator and any leftover positional parameters
    OPTRET+=('--' "${unused_argv[@]}" "$@")
    unset longoptmatch

    return 0
}

function cleanup()
{
    exit ${1:-$?}
}

function usage()
{
    cat <<EOF
使用: ${0##*/} [配置选项]

  配置选项:
   -u,  --update                     更新本地基金列表
   -n,  --name <fund name>           根据基金名字获取基金ID
   -w,  --net-worth <fund code>      根据基金ID获取净值
   -W,  --net-worth-days <fund code> 根据基金ID获取净值，可以添加'时间范围(例如: 10d)'参数
   -h,  --help                       显示此帮助信息并退出

EOF
}


function update_fund_list()
{
    ${pythoncmd} "${fundListPython}" "${fundListFile}"
}

function fund_name_by_code()
{
    ${pythoncmd} "${fundInfoPython}" "$1" "${fundListFile}"
}

function fund_worth_by_code()
{
    [[ x"$2" == x'' ]] && ${pythoncmd} "${fundWorthPython}" "$1" "${dataDir}"
    [[ x"$2" != x'' ]] && ${pythoncmd} "${fundWorthPython}" "$1" "${dataDir}" "$2"
}

function fund()
{
  exit 0

}

### main
trap 'cleanup 130' INT
trap 'cleanup 143' TERM

if [ "$#" -lt 1 ]; then
    usage
    cleanup 1
fi

_opt_short='n:w:W:hu'
_opt_long=('name:' 'net-worth:' 'net-worth-days:' 'help' 'update')

parseopts "$_opt_short" "${_opt_long[@]}" -- "$@" || exit 1
set -- "${OPTRET[@]}"
unset _opt_short _opt_long OPTRET

while :; do
    case $1 in
        -u|--update)
            update_fund_list
            cleanup 0
            ;;
        -n|--name)
            shift
            fund_name_by_code "$1"
            ;;
        -w|--net-worth)
            shift
            fund_worth_by_code "$1"
            ;;
        -W|--net-worth-days)
            shift
            fundCode=$1
            shift
            days="$2"
            days=${days%*d}
            fund_worth_by_code "${fundCode}" "${days}"
            ;;
        -h|--help)
            usage
            cleanup 0
            ;;
        --)
            shift
            break 2
            ;;
    esac
    shift
done

