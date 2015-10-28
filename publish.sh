# Insert a new user
mosquitto_pub -t company/client1/users/new -m '{"data":{"users":{"firstname":"Javier", "lastname":"Aguila", "username":"sjaca10", "email":"javier@kliento.mx", "imei":"12345610654321", "created":"2015-10-22 10:52:36"}}}'

# Insert a ping
mosquitto_pub -t company/client2/aaguila/ping/geo/new -m '{"data":{"ping":{"latitude":"28.48218", "longitude":"104.2194", "created":"2015-10-19 16:37:36"}}}'

# Insert a new user with ping
mosquitto_pub -t company/client1/users/new -m '{"data":{"users":{"firstname":"Javier", "lastname":"Aguila", "username":"sjaca10", "email":"javier@kliento.mx", "imei":"12345610654321", "created":"2015-10-22 10:52:36"}, "ping":{"latitude":"98.18798", "longitude": "108.97256", "created":"2015-10-22 10:52:36"}}}'

# Retrieving users with lastname = Aguila
mosquitto_pub -t company/client1/users -m '{"data":{"users":{"column":"lastname", "filter":"equals", "value":"Aguila"}}}'

# Retrieving ping with id = 1
mosquitto_pub -t company/client2/aaguila/ping/geo -m '{"data":{"ping":{"column":"id", "filter":"equals", "value":"1"}}}'

# Deleting user with id = 1
mosquitto_pub -t company/client1/users/delete -m '{"data":{"users":{"column":"id", "filter":"equals", "value":"1"}}}'

# Deleting ping with id = 1
mosquitto_pub -t company/client2/aaguila/ping/geo/delete -m '{"data":{"ping":{"column":"id", "filter":"equals", "value":"1"}}}'

# Update user with id = 2
mosquitto_pub -t company/client1/users/update -m '{"data":{"users":{"search":"lastname", "filter":"equals", "value":"Aguila", "update":"firstname", "new":"JACA"}}}'