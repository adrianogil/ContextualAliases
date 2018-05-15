alias ctx-actions='python $CONTEXTUAL_ALIASES_DIR/src/context_aliases.py'
alias ctx-update='source $CONTEXTUAL_ALIASES_DIR/src/bashrc.sh'

function execute_contextual_action()
{
    action_alias=$1
    action_command=$(python $CONTEXTUAL_ALIASES_DIR/src/context_aliases.py -c $action_alias)
    echo "Contextual action: "$action_command
    echo ""
    eval $action_command
}

all_ctx_aliases=$(python2 $CONTEXTUAL_ALIASES_DIR/src/context_aliases.py -u)
for a in $all_ctx_aliases ; do
    alias $a="execute_contextual_action $a"
done