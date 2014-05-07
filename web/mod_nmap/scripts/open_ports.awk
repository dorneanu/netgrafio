# @Author: victor
# @Date:   2014-04-22
# @Last Modified by:   victor
# @Last Modified time: 2014-04-23
# @Copyright:
#
#    This file is part of the netgrafio project.
#
#
#    Copyright (c) 2014 Victor Dorneanu <info AAET dornea DOT nu>
#
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included in all
#    copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#    SOFTWARE.
#
#    The MIT License (MIT)

BEGIN { OFS=" "; }
{
	host=$6;
	status=$2;

	# Extract port / protocol pairs
	split($4, p, "/");
	port=p[1];
	proto=p[2];

	# Generate unique IDs for the nodes
	status_id= host "::status::" status;
	proto_id = host "::proto::" proto;
	port_id = host "::port::" port;

	# Print nodes
	printf "{\"nodes\":["
	printf "{\"name\":\"%s\", \"class\":\"host\"},", host
	printf "{\"name\":\"%s\", \"class\": \"port\", \"id\": \"%s\"},", port, port_id
	printf "{\"name\":\"%s\", \"class\": \"proto\", \"id\": \"%s\"},", proto, proto_id
	printf "{\"name\":\"%s\", \"class\":\"status\", \"id\":\"%s\"}", status, status_id
	printf "],"

	# Print links
	printf "\"links\":["
	printf "{\"source\":\"%s\", \"target\":\"%s\", \"linkclass\": \"host-status\"},", host, status_id
	printf "{\"source\":\"%s\", \"target\":\"%s\", \"linkclass\": \"status-proto\"},", status_id, proto_id
	printf "{\"source\":\"%s\", \"target\":\"%s\", \"linkclass\": \"proto-port\"}", proto_id, port_id

	# Finish JSON packet
	printf "]}"
	printf "\n"
}
END {}
