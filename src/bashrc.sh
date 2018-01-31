alias ctx-actions='python $CONTEXTUAL_ALIASES_DIR/src/context_aliases.py'
alias ctx-update='source $CONTEXTUAL_ALIASES_DIR/src/bashrc.sh'

all_ctx_aliases=$(python $CONTEXTUAL_ALIASES_DIR/src/context_aliases.py -u)
for a in $all_ctx_aliases ; do
    alias $a="python $CONTEXTUAL_ALIASES_DIR/src/context_aliases.py -e $a"
done