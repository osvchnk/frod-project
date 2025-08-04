#!/bin/bash

NAMENODE_DIR="/tmp/hadoop-root/dfs/name"

# Only format if it hasn't already been formatted
if [ ! -d "$NAMENODE_DIR/current" ]; then
  echo "Formatting HDFS NameNode..."
  hdfs namenode -format -nonInteractive
fi

# Start the NameNode
exec hdfs namenode