rm stio.*
export LAAB_LOG_DIR=.
srun -A cstao -N 2 -n 6 stiorw ls
