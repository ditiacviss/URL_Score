import pandas as pd
from features.new import get_security_headers, get_meta_tags, get_content_ratio

df = pd.read_csv("data/data_details_new1.csv")

url_list = []
security_headers_list = []
meta_tags_list = []
content_ratio_list = []

for count, url in enumerate(df["Url"]):
    print(f"Processing count {count} for URL: {url}")

    security_headers = get_security_headers(url)
    meta_tags = get_meta_tags(url)
    content_ratio = get_content_ratio(url)

    print("Meta Tags:", meta_tags)
    print("Content Ratio:", content_ratio)
    print("Security headers:", security_headers)

    url_list.append(url)
    security_headers_list.append(security_headers)
    meta_tags_list.append(meta_tags)
    content_ratio_list.append(content_ratio)

    data = {
        "Url": url_list,
        "Security Headers": security_headers_list,
        "Meta Tags": meta_tags_list,
        "Content Ratio": content_ratio_list
    }

    temp_df = pd.DataFrame(data)
    temp_df.to_csv(f"temp2/data_{count}.csv", index=False)

print("Processing complete.")
