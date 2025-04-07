#!/usr/bin/env python3
import datetime
from mcp.server.fastmcp import FastMCP

#mcp = FastMCP("Datetime", host="0.0.0.0", port=8000, debug=True, log_level="DEBUG")
mcp = FastMCP("Datetime")

@mcp.tool()
def echo_datetime() -> str:
	"""Return datetime"""
	return str(datetime.datetime.now())

if __name__ == "__main__":
	mcp.run('sse')
