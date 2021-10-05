#!/bin/bash
# Clone the tig-stack forked repository and change into directory
git clone https://github.com/nickrusso42518/tig-stack.git
cd tig-stack/

# Start the TIG stack in the background
docker-compose up --detach

# Check to see that TCP ports 42518, 3000, 8083, and 8086 are open
ss -tna
