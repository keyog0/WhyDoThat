use keyog;
drop table if exists job_detail;
create table job_detail (
    job_item_id int unsigned not null auto_increment primary key,
    job_item_title varchar(500) not null,
    job_item_href varchar(500),
    job_item_main_text text not null,
    job_item_salary varchar(50),    
    job_item_skill_tag varchar(500),
    job_item_sector varchar(200),
    job_item_newbie boolean,
    job_item_career varchar(50),
    job_item_deadline date,
    company_name varchar(100),
    company_address varchar(500),
    platform varchar(100),
    job_item_logo varchar(500)
) DEFAULT CHARSET=utf8mb4;
desc job_detail;
select * from job_detail;