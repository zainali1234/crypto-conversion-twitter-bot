from bs4 import BeautifulSoup
import requests

# checks if the value is a float
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

# converts number to a float
def convert_to_float(stringVal):
    if '$' in stringVal:
        stringVal = stringVal.replace('$', '')
    if ',' in stringVal:
        stringVal = stringVal.replace(',', '')
    return float(stringVal)

# scrapes crypto website and returns the price values of the crypto
# we have to search for
def scrape_website(request_to_convert_from, request_to_convert_to, is_symbol):
    web_page_num = 1
    coin_num = 1
    price_to_convert_from = 0.0
    price_to_convert_to = 0.0
    from_price_found = False
    to_price_found = False

    while (web_page_num <= 101):
        website = 'https://coinmarketcap.com/?page=' + str(web_page_num)
        response = requests.get(website)
        soup = BeautifulSoup(response.content, 'html.parser')

        coin_name_data_base = soup.find('table', class_='h7vnx2-2 czTsgW cmc-table').find('tbody').find_all('tr')
        price = 0.0
        for coin in coin_name_data_base:
            coinAttributes = coin.find_all('td')
            if(is_symbol is not True):
                coin_name = coinAttributes[2].find('p', class_='sc-1eb5slv-0 iworPT')
                if coin_name is None:
                    coin_name = coinAttributes[2].find_all('span')
                    coin_name = coin_name[1]
                coin_name = coin_name.text.lower()
            else:
                coin_name = coinAttributes[2].find('p', class_='sc-1eb5slv-0 gGIpIK coin-item-symbol')
                if coin_name is None:
                    coin_name = coinAttributes[2].find_all('span')
                    coin_name = coin_name[2]
                coin_name = coin_name.text.lower()
            price = coinAttributes[3].find('span').text
            if coin_name == request_to_convert_from:
                price_to_convert_from = price
                from_price_found = True
            if coin_name == request_to_convert_to:
                price_to_convert_to = price
                to_price_found = True
            coin_num = coin_num + 1
            if from_price_found and to_price_found:
                break
        if from_price_found and to_price_found:
            break
        web_page_num = web_page_num + 1

    return price_to_convert_from, price_to_convert_to

# converts user entered string into usable values for conversion
def format_extraction(text_request):
    num_to_convert = 0.0
    request_to_convert_from = " "
    request_to_convert_to = " "
    is_symbol = True

    for value in text_request.split(" "):
        if value.isdigit() or isfloat(value):
            num_to_convert = value
            i = text_request.split(" ").index(value)
            request_to_convert_from = text_request.split(" ")[i + 1].replace('_'," ")
            request_to_convert_to = text_request.split(" ")[i + 3].replace('_', " ")
            if (((request_to_convert_from.isupper()) is not True) or (request_to_convert_to.isupper()) is not True):
                is_symbol = False
            request_to_convert_from = request_to_convert_from.lower()
            request_to_convert_to = request_to_convert_to.lower()
    return num_to_convert,request_to_convert_from, request_to_convert_to, is_symbol

# receives the searched name and price values, and returns output string
# with the converted value
def convert_crypto(text_request):
    num_to_convert, request_to_convert_from, request_to_convert_to, is_symbol = format_extraction(text_request)
    price_to_convert_from, price_to_convert_to = scrape_website(request_to_convert_from, request_to_convert_to, is_symbol)
    if (price_to_convert_from == 0.0) and (price_to_convert_to != 0.0):
        return ("Sorry, I couldn't find specified crypto, " + '\"' + str(
            request_to_convert_from) + '\"' + ", please try again.")
    elif (price_to_convert_from != 0.0) and (price_to_convert_to == 0.0):
        return ("Sorry, I couldn't find specified crypto, " + '\"' + str(
            request_to_convert_to) + '\"' + ", please try again.")
    elif (price_to_convert_from == 0.0) and (price_to_convert_to == 0.0):
        return ("Sorry, I couldn't find specified cryptos," + '\"' + str(request_to_convert_to) + '\"' +
                " and " + '\"' + str(request_to_convert_from) + '\"' + ", please try again.")
    else:
        final_conversion_value = (convert_to_float(num_to_convert) * (convert_to_float(price_to_convert_from))
                                  / convert_to_float(price_to_convert_to))
        if(is_symbol):
            request_to_convert_from = request_to_convert_from.upper()
            request_to_convert_to = request_to_convert_to.upper()
        return (str(num_to_convert) + " " + request_to_convert_from + " is currently worth approximately "
                + str(round(final_conversion_value, 5)) + " " + request_to_convert_to + "!")
