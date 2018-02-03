sh -p 23579 jihun@memorist.xyz -i ~/.ssh/id_memorist -o StrictHostKeyChecking=no <<'ENDSSH'
./run_server.sh
exit
ENDSSH
