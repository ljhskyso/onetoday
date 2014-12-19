DROP DATABASE twitter_bot;
CREATE DATABASE twitter_bot;
USE twitter_bot;
CREATE TABLE t_User (
    user_id INT AUTO_INCREMENT,
    twitter_id INT UNIQUE,
    twitter_screenname VARCHAR(50) UNIQUE,
    google_id INT,
    google_username VARCHAR(50),
	post_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    flg_active BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (user_id)
);
CREATE TABLE t_Twt_Receied (
    twt_received_id INT AUTO_INCREMENT,
    received_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    post_user_id INT NOT NULL,
    twt_received VARCHAR(200) NOT NULL,
    hash_tag_cnt INT NOT NULL,
    flg_active BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (twt_received_id),
    FOREIGN KEY (post_user_id)
        REFERENCES t_User (user_id)
);
CREATE TABLE t_Twt_Reply (
    twt_reply_id INT AUTO_INCREMENT,
    reply_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    receive_user_id INT NOT NULL,
    project_id INT NOT NULL,
    twt_reply VARCHAR(200) NOT NULL,
    flg_active BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (twt_reply_id),
    FOREIGN KEY (receive_user_id)
        REFERENCES t_User (user_id)
);
CREATE TABLE t_Hashtag_In_Twt_Received (
	hashtag_in_twt_id INT AUTO_INCREMENT,
    twt_received_id INT NOT NULL,
    hash_tag VARCHAR(200) NOT NULL,
    twt_reply_id INT,
	flg_active BOOLEAN DEFAULT TRUE,
	PRIMARY KEY (hashtag_in_twt_id)
);
