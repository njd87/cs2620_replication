# How to Start

Run all 5 servers in 5 terminals:

```console
python3 server.py 0
```

```console
python3 server.py 1
```

```console
python3 server.py 2
```

```console
python3 server.py 3
```

```console
python3 server.py 4
```

The indices correspond to the hosts and ports in config.

Running a client is simple:

```console
python3 client.py
``` 

It will automatically connect and find new leader whenever needed. Feel free to change host and port numbers.

# How to Use

Interact via tkinter window to enter username, login/register. Then, select from available users and click the "message" button to start messaging them on the right hand side by clicking "send message" when message is type.

Click settings to start account deletion.

Click messages sent by you and click "delete message" to delete them.