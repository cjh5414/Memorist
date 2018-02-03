#!/bin/bash
ssh -p 23579 jihun@memorist.xyz -i ~/.ssh/id_memorist -o StrictHostKeyChecking=no <<'ENDSSH'
./Memorist/scripts/run_server.sh
exit
ENDSSH
