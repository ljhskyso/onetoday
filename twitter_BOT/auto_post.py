from post import post_tweet

import json
from apiclient.discovery import build
# from getPictures import getPictures

import peewee
from peewee import *
# db = MySQLDatabase('twitter_bot', user='root',passwd='onetoday@CT')
db = MySQLDatabase('twitter_bot', host="2cood.com", port=3306, user="ct.onetoday", passwd="onetoday@CT")

import tweepy
import urllib
from datetime import datetime
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import sys

from oauth2client import client
from googleapiclient import sample_tools

sys.path.append('./OAuth2')
from onetoday_projectsGet import api_projects_get
from onetoday_projectsGet import api_projects_get_target_unit

# from main import listRecent20DonorsFromOfferId
# from main import combine_all_icons


#################################################################
# NEW PROJECT OF THE WEEK

def post_proj_new( proj_keyword ):
    print 'Posting new Project-Of-The-Week...'
    print '----------------------------------'
    print
    
    # read mannual process first
    sql = 'SELECT MIN(auto_id) FROM t_autopost WHERE flg_posted = 0'
    rsp = db.execute_sql( sql ).fetchall()
    auto_id = rsp[0][0]
    
    print 'record # of: ' + str(auto_id)
    
    # handle the case of no mannual input
    if auto_id == None:
        [ url, prj_name, photo_file, prj_id ] = get_project( proj_keyword )        
        tweet_content = 'This is the project of this week! Help us at ' + url + ' You can help to make this dream come true!'
        prj_goal = api_projects_get_target_unit(prj_id, sys.argv)
        
        print('replying: ' + tweet_content)
        print '          ' + photo_file
        
        # store the post to DB as a record
        sql = 'INSERT INTO t_autopost (flg_posted, post_img, post_txt, post_proj_nm, post_proj_id, post_proj_url, post_proj_goal) VALUES (1, ' + '"' + photo_file + '", ' + '"' + tweet_content + '", ' + '"' + prj_name + '", ' + '"' + prj_id + '", ' + '"' + url + '", ' + '' +  str(prj_goal) + ')'
        db.execute_sql( sql )
    
    
    # tweet image
    [amt_unitCost, cur_unitCost, unitQuantity, unit, amt_totalDonated, cur_totalDonated, donorsCount] = api_projects_get(prj_id, sys.argv)

    print
    img_txt = []
    
    img_txt.append(prj_name)
    img_txt.append('TOGETHER')
    img_txt.append('WE CAN DO MORE')

    x = amt_totalDonated / amt_unitCost * unitQuantity
    img_txt.append('That is ' + str(x) + ' ' + unit + '.')
    img_txt.append(str(amt_unitCost) + ' ' + cur_unitCost + ' = ' + str(unitQuantity) + ' ' + unit)
    
    img_txt.append('What can you do? Help us to reach our goal!')
    img_txt.append('We need ' + str(prj_goal) + ' meals this week!')
    img_txt.append('We count on you!')
    
    print img_txt
    
    
    
    # make the post
    new_img = process_img_add_text(img_txt, photo_file, "new", prj_id)
    post_tweet(new_img, tweet_content, None)
    
    
    
    
    
    
    
    print
    print 'Completed new Project-Of-The-Week...'
    print '==================================================================='
    print
    
    
    
#################################################################
# UPDATE PROJECT OF THE WEEK

def post_proj_update():
    print 'Posting updates to Project-Of-The-Week...'
    print '-----------------------------------------'
    print
    
    # find current running project_id
    auto_id = find_current_running_project()    
    [prj_id, prj_url, prj_name, prj_goal, prj_img] = find_info_by_auto_id( auto_id )
    
    # tweet text
    tweet_content = 'How we are doing: Help us at ' + prj_url + ' You can help to make this dream come true!' + "for" + prj_name
    print tweet_content
    
    # tweet image
    [amt_unitCost, cur_unitCost, unitQuantity, unit, amt_totalDonated, cur_totalDonated, donorsCount] = api_projects_get(prj_id, sys.argv)
    
    print
    img_txt = []
    img_txt.append(prj_name)
    img_txt.append('TOGETHER')
    img_txt.append('WE CAN DO MORE')
   
    img_txt.append(str(donorsCount) + ' people have helped raise ' + str(amt_totalDonated) + ' ' + cur_totalDonated + '.')
   
    x = amt_totalDonated / amt_unitCost * unitQuantity
    img_txt.append('That is ' + str(x) + ' ' + unit + '.')
    img_txt.append(str(amt_unitCost) + ' ' + cur_unitCost + ' = ' + str(unitQuantity) + ' ' + unit)
   
    img_txt.append('What can you do? Help us to reach our goal!')
    img_txt.append('We need ' + str(prj_goal) + ' meals this week!')
    img_txt.append('We count on you!')
    
    print img_txt
    
    new_img = process_img_add_text(img_txt, prj_img, "update", prj_id)
    
    print "making the post..."
    # post_tweet(new_img, tweet_content, None)
    
    print
    print 'Completed update Project-Of-The-Week...'
    print '==================================================================='
    print
    
    

#################################################################
# END PROJECT OF THE WEEK

def post_proj_result():
    print 'Posting result of Project-Of-The-Week...'
    print '----------------------------------------'
    print
    
    # find current running project_id
    auto_id = find_current_running_project()
    # print auto_id
    
    [prj_id, prj_url, prj_name, prj_goal, prj_img ] = find_info_by_auto_id( auto_id )
    [amt_unitCost, cur_unitCost, unitQuantity, unit, amt_totalDonated, cur_totalDonated, donorsCount] = api_projects_get(prj_id, sys.argv)
    x = amt_totalDonated / amt_unitCost * unitQuantity
    
    
    # # get donors pics ----------------------
    # listRecent20DonorsFromOfferId(prj_id, sys.argv)
    # print combine_all_icons()
    
    
    if ( x >= prj_goal):
        # Goal was reached
        
        # tweet text
        tweet_content = 'You all are Heroes!'
        print tweet_content
        
        # tweet image
        img_txt = []
        img_txt.append('- Thank you for helping us reach our goal! -')
    
        img_txt.append(prj_name)
        img_txt.append('TOGETHER')
        img_txt.append('WE CAN DO MORE')
        img_txt.append(str(donorsCount) + ' people have helped raise ' + str(amt_totalDonated) + ' ' + cur_totalDonated + '.')
        img_txt.append('That is ' + str(x) + ' ' + unit + '.')
        
        print img_txt

    else:
        # Goal was NOT reached
    
        # tweet text
        tweet_content = 'Together we can still doing more!  Continue supporting us at ' + prj_url + "for" + prj_name
        print tweet_content
    
        # tweet image
        img_txt = []
        img_txt.append('- Thank you for helping us! -')
        
        img_txt.append(prj_name)
        img_txt.append(str(donorsCount) + ' people have helped raise ' + str(amt_totalDonated) + ' ' + cur_totalDonated + '.')
        img_txt.append('That is ' + str(x) + ' ' + unit + '.')
        img_txt.append('TOGETHER')
        img_txt.append('WE CAN DO MORE')
    
        print img_txt
    
    # add text to the image
    new_img = process_img_add_text(img_txt, prj_img, "end", prj_id)
    
    print "making the post"
    print new_img
    print tweet_content
    
    print "posting tweets..."
    post_tweet(new_img, tweet_content, None)
    
    
    # update the record to mark the project to be ended
    sql = 'UPDATE t_autopost SET flg_completed = 1 WHERE auto_id = ' + str(auto_id)    
    db.execute_sql( sql )
    
        
    print
    print 'Completed result Project-Of-The-Week...'
    print '==================================================================='
    print
    
    
#################################################################
# some private functions

# find one project to be posted as project-of-the-week
def get_project( keyword ):
    
    print('finding project of the week for: ' + keyword)

    service = build('onetoday', 'v1', developerKey='AIzaSyChpIe6eRbzRDlgMecR3IsMBZmWb1WG2Cw')
    
    url = None
    prj_name = None
    photo_path = None
    prj_id = None

    if keyword != ' ':
        s_resp =  service.projects().search( query=keyword ).execute()

        if 'projects' in s_resp:
            
            for project in s_resp["projects"]:
                print project["tagLine"]
                # project = s_resp["projects"][0]
                prj_id = project["id"]
                
                # continue if the project has never been posted, otherwise, use next project
                if prj_not_posted(prj_id):
                    url = project["projectUrl"]
                    prj_name = project["tagLine"]
                    prj_photo_url = project["photoUrl"]
                    photo_path = process_image(prj_photo_url)
                
                    print
                    print 'project name: ' + prj_name
                    print
                    
                    break
        else:
            print
            print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            print "ERROR!!! NO PROJECT FOUND! PLEASE TRY AGAIN!"
            print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            print
            sys.exit()

    else:
        print
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print "ERROR!!! NO KEYWORD FOUND! PLEASE TRY AGAIN!"
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print
        sys.exit()
        
        
    if (url == None or prj_name == None or photo_path == None or prj_id == None):
        print
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print "ERROR!!! ALL PROJECT POSTED! PLEASE TRY AGAIN!"
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print
        sys.exit()
        

    return [ url, prj_name, photo_path, prj_id ]


# process the image
def process_image(photo_url):
	i = datetime.now()
	now = i.strftime('%Y%m%d-%H%M%S')
	photo_name = './images_weekly_project/' + now + '.jpg'
	urllib.urlretrieve(photo_url, photo_name)
	

	#new_image manipulation
	fontsize = 28
	font = ImageFont.truetype("Ayuthaya.ttf", fontsize)
	img = Image.open(photo_name)
	(width, height) = img.size
	heightZ = height
	widthZ = width / 2
	logo = Image.open('./backPicture2.png')
	(logow, logoh) = logo.size
	print logo.mode
	

	#resize logo according to needs
	logo2 = logo.resize((width, ((logoh*width)/logow)), Image.ANTIALIAS)
	(logo2w, logo2h) = logo2.size	

	#inserting logo on pictures
	offset = ((width - logo2w)/2, (height - logo2h)/2)  
	img.paste(logo2, offset, mask=logo2)	
	


	#draw = ImageDraw.Draw(img)
	#draw.text((0, height), "Be the #Hero today!",(255,255,255), font=font )
	img.save(photo_name)

	return photo_name




# check if the project has been posted before as Project-Of-The-Week
def prj_not_posted(prj_id):
    sql = 'SELECT COUNT(*) FROM t_autopost WHERE post_proj_id = ' + '"' + prj_id + '"'    
    rsp = db.execute_sql( sql ).fetchall()
    cnt = rsp[0][0]
    
    if (cnt == 0):
        return True
    else:
        return False

def find_current_running_project():
    sql = 'SELECT auto_id FROM t_autopost WHERE flg_posted = 1 AND flg_completed = 0'    
    rsp = db.execute_sql( sql ).fetchall()
    
    if len(rsp) == 1:
        auto_id = rsp[0][0]
        
    elif len(rsp) == 0:
        print
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print "DATA ERROR!!! NO RUNNING PROJECT FOUND!"
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print
        sys.exit()
    else:
        print
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print "DATA ERROR!!! FOUND MULTIPLE RUNNING PROJECTS!"
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print
        sys.exit()
        
    return auto_id
    
    
def find_info_by_auto_id( auto_id ):
    sql = 'SELECT post_proj_id, post_proj_url, post_proj_nm, post_proj_goal, post_img FROM t_autopost WHERE auto_id = ' + str(auto_id)    
    rsp = db.execute_sql( sql ).fetchall()
    
    if len(rsp) == 1:
        prj_id = rsp[0][0]
        prj_url = rsp[0][1]
        prj_name = rsp[0][2]
        prj_goal = rsp[0][3]
        prj_img = rsp[0][4]
        
    elif len(rsp) == 0:
        print
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print "DATA ERROR!!! NO RUNNING PROJECT FOUND!"
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print
        sys.exit()
    else:
        print
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print "DATA ERROR!!! FOUND MULTIPLE RUNNING PROJECTS!"
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print
        sys.exit()
        
    return [prj_id, prj_url, prj_name, prj_goal, prj_img]



      
      

def process_img_add_text( img_txt, img_path, type, prj_id ):
 
    img = Image.open(img_path)
    (width, height) = img.size
    
    # get the new image height
    header_height = 10
    footer_height = 10
    fontsize = 10
    font = ImageFont.truetype("Ayuthaya.ttf", fontsize)    
    twidth, theight = font.getsize(" ")
    txt_height = len(img_txt) * theight
        
    # donor pic size
    donor_w = width
    donor_h = donor_w / 4 * 5
    
    # create the new image
    if type == "end":
        new_img = Image.new('RGB', (width,height + txt_height + header_height + footer_height + donor_h + footer_height), (255,255,255))
    else:
        new_img = Image.new('RGB', (width,height + txt_height + header_height + footer_height), (255,255,255))
        
    
    # add the text
    draw = ImageDraw.Draw(new_img)
    h = header_height
    w = width
    y_text = h
    for line in img_txt:
        twidth, theight = font.getsize(line)
        draw.text(((w - twidth)/2, y_text), line, (0,0,0), font=font)
        y_text += theight
    
    # paste the old image
    new_img.paste( img, (0, y_text + footer_height) )
    
    if type == "end":    
        # paste donor pics
        img = Image.open('./images_recent_donors/recentdonors.jpg')
        re_img = img.resize((donor_w, donor_h), Image.ANTIALIAS)
        new_img.paste( re_img, (0, y_text + footer_height + footer_height + height) )
    
    # save the new image
    photo_name = img_path.replace(".jpg", "_"+type+".jpg")
    new_img.save(photo_name)
    
    return photo_name
    
#################################################################

def main( keyword, args ):
    if args ==  'NEW':
        post_proj_new( keyword )
    elif args == 'UPDATE':
        post_proj_update()
    elif args == 'END':
        post_proj_result()


if __name__ == '__main__':
    # main( args )
    
    # main( "school", 'NEW' )
    main( 'UPDATE' )
    # main( 'END' )