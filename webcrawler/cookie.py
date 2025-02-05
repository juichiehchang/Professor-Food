import pickle

def save_cookie(driver, path):
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

def load_cookie(driver, path):
     with open(path, 'rb') as cookiesfile:
         cookies = pickle.load(cookiesfile)
         for cookie in cookies:
             # drop the expire key
             if 'expiry' in cookie:
                 del cookie['expiry']
             driver.add_cookie(cookie)
