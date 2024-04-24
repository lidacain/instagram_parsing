from bs4 import BeautifulSoup

html_code = '''
<div class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1">
    <!-- Другие элементы внутри -->
    <span class="x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj" dir="auto" style="line-height: var(--base-line-clamp-line-height); --base-line-clamp-line-height: 18px;">
        <span class="x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm x1roi4f4 x10wh9bi x1wdrske x8viiok x18hxmgj" dir="auto" style="line-height: var(--base-line-clamp-line-height); --base-line-clamp-line-height: 18px;">
            Hallo Herr Diesel das ist ein sehr schöner Baum 😍
        </span>
    </span>
    <!-- Другие элементы внутри -->
</div>
'''

soup = BeautifulSoup(html_code, 'html.parser')

# Найти элемент span с классом x1lliihq и извлечь текст комментария
comment_span = soup.find('span', class_='x1lliihq')
if comment_span:
    comment_text = comment_span.get_text(strip=True)
    print(comment_text)
else:
    print('Комментарий не найден')
