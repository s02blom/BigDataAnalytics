#!/usr/bin/env bash

sendFile() {
  # echo "Sending file" "$1" to "$TARGET"
  curl -s -F "name=$1" -F "data=@$1" "$TARGET"
  sleep 0.01  # A slight delay is necessary here to not overrun buffers in the consumer
}


if [[ "$DELAY" == "" ]]; then
 DELAY=0
fi

echo "Stream-of-Code generator."
echo "Delay (seconds) between each file is:" $DELAY
echo "files are sent to                   :" $TARGET

echo "Waiting 5 seconds to give consumer time to get started..."
sleep 5


for i in {1..100000}
do
    sendFile ./test/E.java
    sleep $DELAY
done

echo "No more files to send. Exiting."
