from crawler import Crawler

crawler = Crawler("https://fptshop.com.vn/dien-thoai",
                  "D:/application/chromedriver-win64/chromedriver.exe",
                  scroll_pause_time=1.2)
product_links = crawler.crawl_product_links(num_product_pages=20,
                           product_style=".group.flex.h-full.flex-col.justify-between.ProductCard_brandCard__VQQT8.ProductCard_cardDefault__km9c5",
                           button_style="Button_root__LQsbl.Button_btnSmall__aXxTy.Button_whitePrimary__nkoMI.Button_btnIconRight__4VSUO.border.border-iconDividerOnWhite.px-4.py-2")

if len(product_links) == 0:
    print("No product links found!")
else:
    print(f"Finished collecting product links! {len(product_links)} links")