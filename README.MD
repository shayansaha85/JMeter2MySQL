# JMeter2MySQL

**Description**
--

This is a project I did for createing a webservice, that can extract statistics from a JTL file and send the results in a MySQL database table.

<br/>
<br/>
**How to use?**
--

- First install python from https://www.python.com
- Clone the repository using this command

```bash
git clone ...
```
- Install the dependencies with this command

```bash
pip install -r requirements.txt
```
- Add database configuration details in the *connection.properties* file
- Run *app.py* file with this command

```bash
python app.py
```
- Open postman or any other API testing client and follow below steps
    - Endpoint : **https://<YOUR_IP_ADDRESS>:7171/insert**
    - Method : **POST**
    - Payload

    ```json
    {
        "jtl_path" : "/path/of/jtl_file/FILENAME.jtl",
        "jmeter_bin" : "/path/of/JMeter/bin/folder" 
    }
    ```
- After execution, results will be pushed to the MySQL database
