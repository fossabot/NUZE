import requests,json,re,os,random,time,sys,io
from bs4 import BeautifulSoup
from selenium import webdriver

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
city_querys = {
                'Sydney':
                    [
                        'Sydney%2C%20New%20South%20Wales%2C%20Australia',
                        'ChIJP3Sa8ziYEmsRUKgyFmh9AQM'
                    ],
                'Newcastle':
                    [
                        'Newcastle%2C%20New%20South%20Wales',
                        'ChIJder1jmgUc2sRQD8zFmh9AQU'
                    ],
                'Wollongong':
                    [
                        'Wollongong%2C%20New%20South%20Wales',
                        'ChIJS8moNtEaE2sRwKgyFmh9AQQ'
                    ],
                'CentralCoast':
                    [
                        'Central%20Coast%2C%20New%20South%20Wales',
                        'ChIJTYgyH_PMcmsRcKgyFmh9AQM'
                    ],
                
}

MonthToNumber = {   
                        'Jun' : 6,
                        'Jul' : 7,
                        'Aug' : 8,
                        'Sep' : 9        
                }

MonthDays = {
                '6' : 30,
                '7' : 31,
                '8' : 31,
                '9' : 30     

            }

def checkout(checkin):
    monthin = checkin[5:7]
    datein = checkin[8:]
    datein = int(datein)
    if datein + 1 <= MonthDays[checkin[6]]:
        dateout = datein + 1
        if dateout < 10:
            dateout = '0' + str(dateout)
        else:
            dateout = str(dateout)
        monthout = monthin
    else:
        dateout = '01'
        monthout = int(monthin) + 1
        if monthout < 10:
            monthout = '0' + str(monthout)
        else:
            monthout = str(monthout)
    checkout = '2019-'+ monthout + '-' + dateout
    return checkout

    

def get_houses_lists(query_city,query_id):
    #url = baseURL + '&place_id={0}&query={1}'.format(query_id,query_city)
    response = requests.get(baseURL)
    data_text = response.text

    #no greedy compile
    remarketing_ids = re.search('"remarketing_ids":\[(.*?)\],',data_text)
    ids_str = remarketing_ids.group(1)
    id_lists = ids_str.split(',')
    #print(id_lists)
    return id_lists


def get_houses_brife_infro(j,houses_information,host_information):
    explore_tabs = j.get('explore_tabs')[0]
    sections = explore_tabs.get("sections")
    for i in sections:
        if i.get('section_type_uid') == 'PAGINATED_HOMES':
            houses = i.get('listings') 
            for house in houses:
                listing = house.get('listing')
                lat = listing.get('lat')
                lng = listing.get('lng')
                name = listing.get('name')
                picture_urls = listing.get('picture_urls')
                bedroom_label = listing.get('bedroom_label')
                bedrooms = listing.get('bedrooms')
                bathroom_label = listing.get('bathroom_label')
                bathrooms = listing.get('bathrooms')
                beds = listing.get('beds')
                guest_capacity = listing.get('person_capacity')
                house_id = listing.get('id')
                neighborhood = listing.get('neighborhood')
                preview_amenities = listing.get('preview_amenities')
                reviews_count = listing.get('reviews_count')
                star_rating = listing.get('star_rating')
                space_type = listing.get('space_type')

                if 'user' not in listing.keys():
                    print(listing)
                elif 'id' not in listing['user'].keys():
                    print(listing['user'])

                

                host_id = listing.get('user').get('id')
                host_picture_url = listing.get('user').get('thumbnail_url')


                price = house.get('pricing_quote').get('rate').get('amount')
                currency = house.get('pricing_quote').get('rate').get('currency')
                isPlus = 0
                kicker = listing.get('kicker_content')
                if 'kicker_badge' in kicker.keys():
                    isPlus = 1
                information = [
                                [lat,lng],name,picture_urls,bedroom_label,bedrooms,\
                                bathroom_label,bathrooms,beds,\
                                guest_capacity,neighborhood,preview_amenities,\
                                reviews_count,star_rating,space_type,\
                                price,currency,isPlus,host_id
                    ]
                # key = str(lat) + ',' + str(lng)
                # if key in houses_information.keys():
                #     key = str(lat) + '0' + ',' + str(lng) + '0'
                if str(house_id) in houses_information.keys():
                    pass
                else:
                    houses_information[house_id] = information
                    #print(house_id)
                if str(host_id) in host_information.keys() and len(host_information[str(host_id)]['room_ids']) != 0:
                    pass
                else:
                    host_information = host_infro(host_id,host_information,host_picture_url)
                    print(host_information[str(host_id)])
    return houses_information,host_information


# houses_information = {}
# response = requests.get(baseURL)
# j = response.json()
# houses_information = {}
# houses_information = get_houses_brife_infro(j,houses_information)


baseURL = 'https://www.airbnb.com.au/api/v2/explore_tabs?_format=for_explore_search_web&_intents=p1&adults=0&auto_ib=true&children=0&client_session_id=c8b58dfc-fa2b-4d89-8307-3d7b488ee99e&currency=AUD&experiences_per_grid=20&fetch_filters=true&guests=0&guidebooks_per_grid=20&has_zero_guest_treatment=true&infants=0&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_offset='



def get_houses_brife_infro__in_city(city):
    query_city = city_querys[city][0]
    query_id = city_querys[city][1]
    cityURL = '&items_per_grid=18&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en-AU&luxury_pre_launch=false&metadata_only=false&place_id='\
               + str(query_id) + \
                '&query='\
                + str(query_city) +\
                '&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&s_tag=NSN6ItKl&satori_version=1.1.9&screen_height=278&screen_size=large&screen_width=1200&search_type=PAGINATION&section_offset=8&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true&timezone_offset=600&toddlers=0&version=1.5.6'
    file_name = city + '.json'
    houses_information = read_json_file(file_name)
    #houses_information = {}
    #for i in range(17):
    #host_information = read_json_file('host.json')
    host_information = read_json_file('host.json')
    for i in range(17):
        #host_information = read_json_file('host.json')
        offset = 18 * i
        url = baseURL + str(offset) + cityURL
        response = requests.get(url)
        j = response.json()
        houses_information,host_information = get_houses_brife_infro(j,houses_information,host_information)
        write_json_file('host.json',host_information)
    return houses_information,host_information
    

def house_detail_infro(city,houses_information):
    for key in houses_information:
        if len(houses_information[key]) > 20:
            continue
        house_id = key
        NoPlusUrl = 'https://www.airbnb.com.au/rooms/'
        PlusUrl = 'https://www.airbnb.com.au/rooms/plus/'
        Plus = houses_information[key][16]
        if Plus == 1:
            UrlBase = PlusUrl
        else:
            UrlBase = NoPlusUrl
        houseUrl = UrlBase \
                    + str(house_id) \
                    + '?location=' +  str(city_querys['Sydney'][0]) \
                    + '&adults=0&children=0&infants=0&guests=0&toddlers=0&source_impression_id=p3_1560680974_1GDwK67sogRHWqBG'
        house_detail_infro = requests.get(houseUrl).text
        soup = BeautifulSoup(house_detail_infro,'lxml')
        if Plus == 0:
            desc = soup.select('#details')
            if len(desc) == 0:
                description = ''
            else:
                desc = desc[0].encode('utf-8')
                description = re.sub(r'<.*?>','',str(desc))
                description = re.sub(r'Read more about the spaceContact host','',description)
                description = re.sub(r'\\(.*?) ','',description)
                description = re.sub(r'^b\'','',description)
                description = re.sub(r'Contact host','',description)
        else:
            description = soup.find('span',class_ = '_11oyobo').get_text()

        houses_information[key].append(description)
        reviews_count = houses_information[key][11]
        pages = int(reviews_count / 7 )
        wrong_link = 0
        if reviews_count > 0:
            houses_information = house_reviews(city,house_id,houses_information,pages,key)
            if len(houses_information[key]) == 18:
                wrong_link = 1

        else:
            houses_information[key].append({})
        if wrong_link:
            houses_information[key].append(-1)
            file_name = city + '.json'
            write_json_file(file_name,houses_information)
            continue
        clean,calenders = house_calenders(house_id,Plus)
        if clean == -1 and calenders == -1:
            houses_information[key].append(-1)
            file_name = city + '.json'
            write_json_file(file_name,houses_information)
            continue
        houses_information[key].append(calenders)
        houses_information[key].append(clean)
        file_name = city + '.json'
        write_json_file(file_name,houses_information)
    return houses_information

def house_reviews(city,house_id,houses_information,pages,key):
    reviewsUrlbase = 'https://www.airbnb.com.au/api/v2/homes_pdp_reviews?currency=AUD&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en-AU&listing_id='\
            + str(house_id)+  \
            '&_format=for_p3&limit=7&offset='
    comments = {}
    for i in range(pages + 1):
        reviewsUrl = reviewsUrlbase  + str(i * 7) \
                        + '&order=language_country'
        response = requests.get(reviewsUrl)
        if response.status_code != 200:
            return houses_information
        j = response.json()
        reviews = j.get('reviews')
        for review in reviews:
            commemt = review.get('comments')
            #commemt = review.get('comments').encode('utf-8')
            commemt = re.sub(r'\\(.*?) ','',str(commemt))
            commemt = re.sub(r'^b\'','',commemt)
            guest = review.get('reviewer').get('host_name')
            #guest = review.get('reviewer').get('host_name').encode('utf-8')
            guest = re.sub(r'^b\'','',str(guest))
            guest_id = review.get('reviewer').get('id')
            comments[str(guest_id)] = [guest,commemt]
    houses_information[key].append(comments)
    return houses_information
        

# houses_information = get_houses_brife_infro__in_city('Sydney')
# houses_infromation = house_detail_infro('Sydney',houses_information)
# houses_information_json = json.dumps(houses_infromation)
# f = open('dataSydneyreview.json','w')
# f.write(houses_information_json)


# with open("dataSydney.json",'r') as sydney_data:
#     houses_information_sydney = json.load(sydney_data)



def house_calenders(house_id,plus):
    clean = -1
    canlenderUrl = 'https://www.airbnb.com.au/api/v2/calendar_months?_format=with_conditions&count=4&currency=AUD&key=d306zoyjsyarp7ifhu67rjxn52tv0t20' \
                    + '&listing_id=' + str(house_id) \
                    + '&locale=en-AU&month=6&year=2019'
    response = requests.get(canlenderUrl)
    if response.status_code != 200:
        return -1,-1
    j = response.json()
    calender = j.get('calendar_months')
    calenders = {}
    for month in calender:
        mm  = month['abbr_name']
        number = MonthToNumber[mm]
        dd = {}
        for days in month['days']:
            date = days['date']
            m = date[6]
            if int(m) != number:
                continue
            available = days['available']
            if available == 1 and clean == -1:
                out = checkout(date)
                clean = house_clean_fee(house_id,date,out,plus)
                #print(clean)
            price = days['price']['local_price']
            dd[date] = [available,price]
        calenders[mm] = dd
    return clean,calenders


def house_clean_fee(house_id,checkin,checkout,plus):
    if plus == 0:
        additionalUrl = 'https://www.airbnb.com.au/api/v2/pdp_listing_booking_details?_format=for_web_with_date&_intents=p3_book_it&_interaction_type=pageload&_p3_impression_id=p3_1561014490_Kh%2BEG4KS2Yv699UB&_parent_request_uuid=09a530f3-ab4a-4e8f-8833-37c074b11158'\
                        + '&check_in='+ checkin \
                        + '&check_out='+ checkout \
                        + '&currency=AUD&force_boost_unc_priority_message_type=&guests=1&key=d306zoyjsyarp7ifhu67rjxn52tv0t20'\
                        + '&listing_id=' + str(house_id) \
                        + '&locale=en-AU&number_of_adults=1&number_of_children=0&number_of_infants=0&show_smart_promotion=0'
    else:
        additionalUrl = 'https://www.airbnb.com.au/api/v2/pdp_listing_booking_details?_format=for_web_with_date&_intents=p3_book_it&_interaction_type=pageload&_p3_impression_id=p3_1561021930_YRai2nPTedL4LG42&_parent_request_uuid=2ec5d665-c4d5-4f6e-93c6-6f05d231c216'\
                            + '&check_in=' + checkin\
                            + '&check_out=' + checkout\
                            + '&currency=AUD&federated_search_id=cedab671-160a-45ad-8dc6-74d5c419cdc4&force_boost_unc_priority_message_type=&guests=1&key=d306zoyjsyarp7ifhu67rjxn52tv0t20'\
                            + '&listing_id='+ str(house_id)\
                            + '&locale=en-AU&number_of_adults=1&number_of_children=0&number_of_infants=0&search_id=31418da9-4468-a50e-cf68-8906bcb2620f&show_smart_promotion=0'    
    response = requests.get(additionalUrl)
    j = response.json()
    listing = j.get('pdp_listing_booking_details')
    for item in listing:
        clean = item['cleaning_fee_as_guest']
    return clean


def host_infro(host_id,host_infromation,picUrl):
    hostUrl = 'https://www.airbnb.com.au/users/show/'\
                + str(host_id)
    host_detail_infro = requests.get(hostUrl).text
    soup = BeautifulSoup(host_detail_infro,'lxml')
    description = soup.find_all('span',{'class' : '_czm8crp'})
    #print(description)

    self_intro = soup.find_all('div',{'class' : '_11oyobo'})
    if len(self_intro) == 0:
        self_intro = ''
    else:
        self_intro = re.sub(r'\<(.*?)\>','',str(self_intro[0]))

    host_name = soup.find_all('div',{'class':'_1ekkhy94'})
    if len(host_name) == 0:
        host_name = 'hiden'
    else:
        #print(host_name)
        host_name = re.sub(r'\<(.*?)\>','',str(host_name[0]))
        host_name = re.sub(r'Hi\, I\’m ','',host_name)
        #print(host_name)

    rooms = soup.find_all('div',{'class':'_v72lrv'})
    if len(rooms) == 0:
        rooms = soup.find_all('div',{'class':'_1u0tqew','aria-hidden':'false'})
    #print(rooms)
    room_ids = []
    for room in rooms:
        #print(room)
        room_id = re.search('href="/rooms/(.*?)"',str(room))
        room_id = room_id.group(1)
        #print(room_id)
        room_ids.append(room_id)
    #print(rooms)

    button_name = soup.find_all('button',{'type':'button','class':'_1dv8bs9v'})
    if len(button_name) != 0:
        button_name = re.sub(r'\<(.*?)\>','',str(button_name[0]))
        if button_name == 'Learn more':
            self_intro = hide_self_intro(hostUrl)
    #print(self_intro)            
    #webdriver click "readmore" button got whole infromation
    host_detail = []
    for des in description:
        des = re.sub(r'\<(.*?)\>','',str(des))
        #print(des)
        host_detail.append(des)

    host_infromation[str(host_id)] = {}
    host_infromation[str(host_id)]['detail'] = host_detail
    host_infromation[str(host_id)]['self_intro'] = self_intro
    host_infromation[str(host_id)]['name'] = host_name
    host_infromation[str(host_id)]['picUrl'] = picUrl
    host_infromation[str(host_id)]['room_ids'] = room_ids
    #print(host_infro[str(host_id)])
    print(host_infromation[str(host_id)])
    return host_infromation

#webdriver click "readmore" button got whole infromation
def hide_self_intro(hostUrl):
    driver = webdriver.Chrome()
    driver.get(hostUrl)
    button = driver.find_element_by_class_name('_1dv8bs9v')
    button.click()        
    soup = BeautifulSoup(driver.page_source,'lxml')
    self_intro = soup.find_all('div',{'class' : '_czm8crp','dir':'ltr','tabindex':'-1'})
    self_intro = re.sub(r'\<(.*?)\>','',str(self_intro[0]))
    #print(self_intro)
    driver.close()
    return self_intro



def read_json_file(file):
    try:
        with open(file,'r') as data:
            information = json.load(data)
    except FileNotFoundError:
        information = {}
    data.close()
    return information


def write_json_file(file,information):
    information_json = json.dumps(information)
    f = open(file,'w')
    f.write(information_json)
    f.close()


#house_clean_fee('7042470','2019-06-20','2019-06-21',1)
#house_calenders('9051847',0)


# houses_information,host_information = get_houses_brife_infro__in_city('Sydney')
# houses_information = house_detail_infro('Sydney',houses_information)

# host_information_json = json.dumps(host_information)
# f = open('host.json','w')
# f.write(host_information_json)
# f.close()

# houses_information_json = json.dumps(houses_information)
# f = open('Sydney.json','w')
# f.write(houses_information_json)
# f.close()



# with open("dataSydney.json",'r') as sydney_data:
#     houses_information_sydney = json.load(sydney_data)

if __name__ == "__main__":

    host = read_json_file('host.json')
    hh = host_infro('30069789',{},'https://a0.muscache.com/im/users/30069789/profile_pic/1427411468/original.jpg?aki_policy=profile_small')
    print(hh)
    for h in hh:
        host['30069789'] = hh[h]
    print(host['30069789'])
    write_json_file('host.json',host)

    
    
    # houses_information,host_information = get_houses_brife_infro__in_city('Sydney')

    # houses_information = read_json_file('Sydney.json')
    # print(len(houses_information))
    # houses_information = house_detail_infro('Sydney',houses_information)
    # write_json_file('Sydney.json',houses_information)
