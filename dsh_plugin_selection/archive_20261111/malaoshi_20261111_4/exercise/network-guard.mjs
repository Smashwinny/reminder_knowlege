// Self-written, process-local test stub. Not an OS firewall or general sandbox.
// No credentials are inspected. Normal network APIs throw and record any attempt.
import http from 'node:http';import https from 'node:https';import net from 'node:net';import tls from 'node:tls';import {syncBuiltinESMExports} from 'node:module';
globalThis.__networkAttempts=[];
const deny=(name)=>(...args)=>{globalThis.__networkAttempts.push(name);throw Error('Test forbids network: '+name)};
globalThis.fetch=deny('fetch');http.request=deny('http.request');http.get=deny('http.get');https.request=deny('https.request');https.get=deny('https.get');net.connect=deny('net.connect');net.createConnection=deny('net.createConnection');net.Socket.prototype.connect=deny('Socket.connect');tls.connect=deny('tls.connect');syncBuiltinESMExports();
