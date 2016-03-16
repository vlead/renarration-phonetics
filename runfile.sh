 #!/bin/bash
tab="--tab"
cmd1="bash -c 'cd Frontend; ./runfile.sh;exit';bash"
cmd2="bash -c 'cd REST-API; ./runfile.sh;exit';bash"
foo=""

#for i in 1 2; do
foo=($tab -e "$cmd1")
#gnome-terminal "${foo[@]}"
foo+=($tab -e "$cmd2")     
gnome-terminal "${foo[@]}"    
#done

#gnome-terminal "${foo[@]}"

exit 0


# cd Frontend
#./runfile.sh
#cd ../
#cd REST-API
#./runfile.sh
#cd ../
