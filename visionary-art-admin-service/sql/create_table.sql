set FOREIGN_KEY_CHECKS = 0;

-- 用户信息表
drop table if exists user;

create table user(
    uid int not null primary key auto_increment,
    name varchar(256) not null,
    password varchar(256) not null,
    sid varchar(256) not null,
    ip varchar(20) not null,
    regdate datetime not null,
    avatar varchar(256),
    stat varchar(20) not null CHECK (stat in ('online', 'offline', 'banned'))
);

-- 模型基本信息
drop table if exists model;

create table model(
    id int not null primary key auto_increment,
    modelname varchar(256) not null,
    type varchar(64) not null,
    size bigint not null,
    path varchar(256) not null,
    url varchar(256) not null,
    cover_pic varchar(256),
    uid int not null,
    liked int not null,
    upload_time datetime not null,
    disc text,
    version varchar(256),
    foreign key(uid) references user(uid)
);

-- 评论基本信息
drop table if exists comment;

create table comment(
    id int not null primary key auto_increment,
    post_time datetime not null,
    ip varchar(20) not null,
    content varchar(256) not null,
    uid int not null,
    mid int not null,
    liked int not null,
    foreign key (uid) references user(uid),
    foreign key (mid) references model(id)
);

-- 模型点赞基本信息
drop table if exists user_like_model;

create table user_like_model(
    uid int not null,
    mid int not null,
    foreign key (uid) references user(uid),
    foreign key (mid) references model(id),
    primary key(uid, mid)
);

-- 评论点赞基本信息
drop table if exists user_like_comment;

create table user_like_comment(
    uid int not null,
    cid int not null,
    foreign key (uid) references user(uid),
    foreign key (cid) references comment(id),
    primary key(uid, cid)
);

--生成图片基本信息
drop table if exists image;

create table image(
    id int not null primary key auto_increment,
    path varchar(256) not null,
    generation_info_html varchar(4096) not null,
    uid int not null,
    foreign key (uid) references user(uid)
);

SET FOREIGN_KEY_CHECKS = 1;