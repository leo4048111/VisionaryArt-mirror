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
) default charset=utf8mb4 collate=utf8mb4_unicode_ci;

-- 模型基本信息
drop table if exists model;

create table model(
    id int not null primary key auto_increment,
    fuid varchar(256) not null,
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
) default charset=utf8mb4 collate=utf8mb4_unicode_ci;

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
) default charset=utf8mb4 collate=utf8mb4_unicode_ci;

-- 模型点赞基本信息
drop table if exists user_like_model;

create table user_like_model(
    uid int not null,
    mid int not null,
    foreign key (uid) references user(uid),
    foreign key (mid) references model(id),
    primary key(uid, mid)
) default charset=utf8mb4 collate=utf8mb4_unicode_ci;

-- 评论点赞基本信息
drop table if exists user_like_comment;

create table user_like_comment(
    uid int not null,
    cid int not null,
    foreign key (uid) references user(uid),
    foreign key (cid) references comment(id),
    primary key(uid, cid)
) default charset=utf8mb4 collate=utf8mb4_unicode_ci;

-- 生成图片基本信息
drop table if exists `image`;

create table image(
    id int not null primary key auto_increment,
    path varchar(256) not null,
    generation_info_html varchar(4096) not null,
    uid int not null,
    foreign key (uid) references user(uid)
) default charset=utf8mb4 collate=utf8mb4_unicode_ci;

-- 管理员信息表
drop table if exists `admin`;

create table admin(
    uid int not null primary key auto_increment,
    name varchar(256) not null,
    password varchar(256) not null,
    stat varchar(20) not null CHECK (stat in ('online', 'offline', 'banned'))
) default charset=utf8mb4 collate=utf8mb4_unicode_ci;

-- 反馈信息表
drop table if exists feedback;

create table feedback(
    id int not null primary key auto_increment,
    uid int not null,
    title varchar(256) not null,
    tag varchar(64) not null,
    contact varchar(256),
    detail text not null,
    post_time datetime not null,
    foreign key (uid) references user(uid)
) default charset=utf8mb4 collate=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;