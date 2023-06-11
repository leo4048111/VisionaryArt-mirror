# VisionaryArt
### 项目开发背景

**随着人工智能技术的飞速发展，AI 绘画技术也日趋成熟。近些日子来，无数精美的 AI 绘画作品都让我们眼前一新。对于没有接触过 AI 绘画领域的小白，他们可能也想体验 AI 绘画的奇妙，但不知从何下手。对于钻研 AI 绘画领域的技术人员，他们可能想分享自己的训练成果，同时和其他从业人员沟通交流，但是缺乏相关的平台。本软件的创建便是为了解决以上问题，为小白和技术人员提供一个在线生成图片，上传分享训练参数并和他人沟通的平台。**

### 项目核心功能需求

+ 用户能够在线欣赏、生成图片，下载相关模型参数
+ 用户能够上传分享自己训练的模型参数
+ 用户能够使用软件系统提供的相关社交功能，与其他用户进行交流

### 核心技术栈
+ 主要开发语言：Python
+ HTTP 服务器：Tornado + FastAPI
+ 前端技术选型：Vue.js + Element UI/HTML + CSS + Js/Gradio
+ 持久层框架：SQLAlchemy
+ 数据库服务：MySQL + Redis
+ 版本管理工具：Git
+ 远程代码托管平台：华为云
+ 接口管理与自动化测试工具：Apifox + Mock.js

### 软件系统功能

+ 主页用户上传文件管理
+ 画廊图片展示
+ 模型上传
+ 模型搜索
+ 在线AI绘图服务

### 使用注意事项

+ 由于服务器带宽有限，我们已经在平台上传了若干大模型供用户使用，建议用户尽量不要上传自己的大模型文件。
+ 如果不知道如何编写AI绘图的Prompt参数，可到画廊中参考其它用户生成的作品参数，或者到模型详情页中仔细阅读每个模型的参数配置建议。
+ 请在Feedback页面留下您的使用反馈，包括功能需求、Bug反馈等。
+ 由于本小组在项目测试过程中服务器流量过大，ECS服务器已经欠费，该项目服务暂时下线

### 开发与维护

本项目根目录下结构基本如下所示：

```sh
│  .gitattributes
│  .gitignore
│  mime.types
│  README.md
│  start_services.sh
│  __init__.py
│
├─sql
├─uploads
├─visionary-art-admin-frontend
├─visionary-art-admin-service
├─visionary-art-ai-service
└─visionary-art-platform
```

其中可见4个visionary-art开头的文件夹：

+ visionary-art-admin-frontend是一个Vue项目，实现了平台后台管理系统的前端功能，需要开发完编译打包，将内容复制黏贴到visionary-art-admin-service下的dist文件夹中
+ visionary-art-admin-service是一个Python Tornado项目，实现了平台的后台管理系统后端
+ visionary-art-ai-service是一个Python Gradio + FastAPI项目，实现了平台的AI画图服务后端
+ visionary-art-platform是一个Python Tornado项目，实现了平台的主要用户界面前端与后端
+ 具体功能实现位置和原理详见项目源码

### 软件系统部署

#### 注意事项

该软件系统服务的部署需要GPU算力环境，请确保您硬件平台的GPU支持至少CUDA11.7以上的CUDA版本，并且已经正确安装cuda。报告下的安装测试流程在环境纯净的Ubuntu 20.04 LTS服务器下测试良好，如果您使用的开发环境不同，并且在部署流程中遇到任何问题，欢迎随时联系我们开发人员交流。

#### 服务部署流程

本项目考虑到甲方的部署便捷性，一共为甲方部署提供了两套方式，甲方可以根据自身对于相关部署技术的熟悉程度，选择任意一套部署工作流进行部署实践操作。

**部署并配置MySQL和Redis服务**

在运行软件系统服务前，必须确保您的运行环境中，MySQL服务和Redis服务已经正确运行在了3306和6379端口上了。如果您的运行环境下还没有配置这两个服务，请跳到**使用Docker部署**章节中查看MySQL和Redis服务的部署方法（或者您可以按照您的开发经验进行部署）。本软件系统配置中默认的数据库连接使用root用户，密码为`123456`。Redis连接使用密码`foobared`，请确保您的数据库配置和这里保持一致。如果您想使用别的密码，相应地需要去项目源码中更改Redis和MySQL数据库的相关配置信息。

**使用本地Python环境部署**

下面，我将先阐述如何在本地部署并运行该项目的相关服务。请先确保您本地安装了版本大于等于3.7的Python环境，具有能够支持cuda11.7以上版本cuda toolkit的GPU硬件设备，并且已经正确安装了版本正确的cuda + cudnn。此处默认您已经进入到了项目源码根目录VisionaryArt下

**①进入项目源码下的visionary-art-platform文件夹并且安装依赖：**

```bash
cd visionary-art-platform
pip install -r requirements.txt
```

**这里如果您的pip是pip3，请自行替换上面的指令或者创建软连接到pip指令，这里不再赘述。如果您的pip提示找不到指定版本的库，请尝试去掉requirements.txt中的版本号指定字段或者自行更换pip源。**

**②运行软件系统用户端网页服务：**

```
python server.py
```

**同样，如果您的python是python3或者其它版本，请自行替换上面的指令或者创建软连接到python指令，这里不再赘述。启动完毕后，您应该可以通过80端口访问到软件系统的用户端网页服务了。**

**③运行软件系统AI画图服务：**

```bash
cd ..
cd visionary-art-ai-service
python run.py
```

**AI画图后端的HTTP服务由FastAPI框架提供，初次启动时不需要您手动使用`pip install -r requirements.txt`命令安装依赖，因为相关的安装命令和版本确认逻辑已经全部实现在了run.py脚本中了。如果安装完毕后依然提示缺少依赖库，您可以再通过pip命令查漏补缺进行安装，此处不再赘述。该服务启动后，会持续向80端口发送心跳确认，同时此时您应该能够在软件系统用户Web界面中访问到AI画图界面了（如果该服务没有启动，用户Web界面会显示该服务当前已下线）**

**④运行软件系统后台管理服务：**

```
cd ..
cd visionary-art-admin-service
python server.py
```

**⑤关闭服务**

```bash
sh kill_services.sh
```

**您可以直接运行项目根目录下的`kill_services.sh`脚本关闭这三个服务，或者您也可以手动在对应服务的终端界面输入ctrl + C信号来终止进程。上述流程结束后，您这边三个服务应该已经全部在正确运行中了。**

##### 使用Docker部署

下面，我将阐述使用Docker image的方式部署本软件系统的具体流程。

**①安装docker：**

1. **更新apt包索引：**

   ````bash
   sudo apt-get update
   ````

2. **安装必备的软件包以允许apt通过 HTTPS 使用存储库（repository）:**

   ```bash
   sudo apt-get install ca-certificates curl gnupg lsb-release
   ```

3. **添加Docker官方版本库的GPG密钥：**

   ```bash
   sudo mkdir -p /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   ```

4. **使用以下命令设置存储库：**

   ```bash
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```

5. **安装最新版本的Docker Engine、containerd 和 Docker Compose：**

   ```bash
   sudo apt-get update
   sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
   ```

6. **验证docker是否安装成功**

   ```bash
   docker version
   ```

7. **安装完成后，运行如下命令验证 Docker 服务是否在运行**

   ```bash
   systemctl status docker
   ```

8. **运行以下命令启动Docker服务**

   ```bash
   sudo systemctl start docker
   ```

9. **设置Docker服务在每次开机时自动启动**

   ```bash
   sudo systemctl enable docker
   ```

10. **验证Docker是否运行正常**

    ```bash
    sudo docker run hello-world
    ```

    此时输出如下，说明docker安装完毕并且运行正常：

    ```bash
    ubuntu@VM-16-10-ubuntu:~$ sudo docker run hello-world
    Unable to find image 'hello-world:latest' locally
    latest: Pulling from library/hello-world
    2db29710123e: Pull complete 
    Digest: sha256:53f1bbee2f52c39e41682ee1d388285290c5c8a76cc92b42687eecf38e0af3f0
    Status: Downloaded newer image for hello-world:latest
    
    Hello from Docker!
    This message shows that your installation appears to be working correctly.
    
    To generate this message, Docker took the following steps:
     1. The Docker client contacted the Docker daemon.
     2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
        (amd64)
     3. The Docker daemon created a new container from that image which runs the
        executable that produces the output you are currently reading.
     4. The Docker daemon streamed that output to the Docker client, which sent it
        to your terminal.
    
    To try something more ambitious, you can run an Ubuntu container with:
     $ docker run -it ubuntu bash
    
    Share images, automate workflows, and more with a free Docker ID:
     https://hub.docker.com/
    
    For more examples and ideas, visit:
     https://docs.docker.com/get-started/
    ```

**②拉取Visionary Art项目的docker image：**随后，您可以使用下列指令流程拉取包含本项目源码的docker镜像并且在docker容器中运行所有的项目服务。

1. **拉取docker镜像**：

   ```bash
   docker pull leo4048111/visionary_art:1.0
   ```

2. **首次运行时，需要通过docker镜像创建并运行一个交互式容器实例，这里将软件系统服务的文件存储路径映射到了宿主机的路径下，您可以根据实际的情况自由更改映射路径：**

   ```bash
   cd /
   mkdir data
   cd data
   mkdir visionary_art_data
   cd visionary_art_data
   mkdir uploads
   mkdir outputs
   docker run -it --network=host --name visionary_art_app -v /data/visionary_art_data/uploads/:/app/VisionaryArt/uploads/ -v /data/visionary_art_data/outputs/:/app/VisionaryArt/visionary-art-ai-service/outputs/ leo4048111/visionary_art:1.0
   ```

   **这里的--name指定了这个container的名字，之后运行则不需要再从镜像创建container实例了，可以直接使用下列命令运行上面创建的容器实例：**

   ```bash
   docker restart visionary_art_app
   docker attach visionary_art_app
   ```

3. **进入交互式容器后，运行软件系统服务：**

   ```bash
   sh /app/VisionaryArt/start_services.sh
   ```

**③安装MySQL服务：**随后，您需要安装并配置MySQL服务，这边建议您依然通过docker容器进行安装，当然您如果想安装在宿主机的物理环境下也是没问题的，这里仅演示通过docker安装的方法：

1. **从Docker Hub上下载MySQL镜像，可以使用以下命令：**

   ```bash
   docker pull mysql
   ```

2. **创建并运行一个新的MySQL容器并指定端口映射和存储地址：**

   ```bash
   docker run --name some-mysql -p 3306:3306 -v /my/mysql/data:/var/lib/mysql -e 
   MYSQL_ROOT_PASSWORD=123456 -d mysql
   ```

   **在这个例子中，我们将MySQL端口映射到主机上的3306端口，并将MySQL数据存储在主机上的/my/mysql/data目录中，当然您也可以随意更改映射到的宿主机数据存储路径来存放MySQL数据。然后，这个MySQL的root密码被设置为了123456，这也是我们项目源码中MySQL源码设置。如果您想设置自己的密码，相应地需要更改项目源码中的数据库账户密码配置，具体方式请与我们开发维护人员联系**

**④安装Redis服务：**随后，您需要在安装并配置Redis服务，这边建议您依然通过docker容器进行安装，当然您如果想安装在宿主机的物理环境下也是没问题的，这里仅演示通过docker安装的方法：

1. **从Docker Hub上下载Redis镜像，可以使用以下命令：**

   ```bash
   docker pull redis
   ```

2. **挂载Redis配置文件：**

   ```bash
   mkdir -p /home/redis/myredis
   cd /home/redis/myredis
   wget https://github.com/leo4048111/my_redis_config/blob/main/redis.conf
   mkdir data
   ```

   **这里您如果照抄上面的命令，则是把redis配置文件放在了/home/redis/myredis下，并且从`https://github.com/leo4048111/my_redis_config/blob/main/redis.conf`上面下载了我们小组开发时所用的redis配置，包括redis用户名密码等重要配置，建议您不要改密码，否则同样地需要到项目源码内修改Redis配置**

3. **启动redis容器：**

   ```sh
   docker run --restart=always --log-opt max-size=100m --log-opt max-file=2 -p 6379:6379 --name myredis -v /home/redis/myredis/myredis.conf:/etc/redis/redis.conf -v /home/redis/myredis/data:/data -d redis redis-server /etc/redis/redis.conf  --appendonly yes  --requirepass 000415
   ```

**⑤验证软件系统：上述部署流程全部完成后，您应该可以通过浏览器访问服务器的80端口，来访问软件系统的AI画图服务功能。同样地，您应该能够通过浏览器访问服务器的7650端口，来访问软件系统的后台管理界面。如果您在部署过程中遇到任何问题，请及时联系开发人员**

### License
```Copyright (c) 2018-2023 leo4048111```

This project is licensed under the AGPL-3.0 license - see the LICENSE file for details.

### Credits
+ https://github.com/AUTOMATIC1111/stable-diffusion-webui
