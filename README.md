# mailgeno
Service that provides distributed system to send emails with various API for your app

---

- [Install](#️-install)
- [Quickstart](#-quickstart)
- [Usage](#-usage)
- [Stack](#-stack)

---

## ⚙️ Install

Pull image from DockerHub:
```bash
docker pull theapplekingy/mailgeno:latest
```

---

## 🚀 Quickstart

You should to provide environment variables using `--env-file` or erumerating `-e`. Required env variables you can see in **.env.test**. This data will be used to connect and login on mail server.

Run the container:
```bash
docker run theapplekingy/mailgeno:latest
```
Requred parameters:
- `-c` - URL on wich mailgeno will work. Default value: `http://localhost:8052`. It means that mailgeno will work for 8052 HTTP port
- `-r` - resource that mailgeno will listen for. Default value: `mail`. It means that your apps can send email using mailgeno via request on `http://<container_hostname>:8052/mail` if `-c` provided to use HTTP. 

In current version mailgeno support integration with RabbitMQ. To use mailgeno with RabbitMQ run:

```bash
docker run theapplekingy/mailgeno:latest -c amqp://<rmq_user>:<rmq_password>@<rmq_host>
```
By default classic durable queue with name **mail** will be created. If need to specify queue name manually provide also `-r`.

---

## 📦 Usage

mailgeno is fully asynchronous service. So when mailgeno get task it starts `asycio.Task` in which mail will be sent. All available interfaces wait json data with fields:
 - **to** - recipient email
 - **topic** - subject of mail
 - **message** - message text of mail

---

## 🧰 Stack

- **aiohttp** – web interface  
- **Docker** – containerization
- **aio_pika** - broker interface 
