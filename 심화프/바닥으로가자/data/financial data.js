import * as pd from 'pandas';
import * as requests from 'requests';
var URL, annual_date, code, df, quater_date, r;
code = "005930";
URL = `https://finance.naver.com/item/main.nhn?code=${code}`;
r = requests.get(URL);
df = pd.read_html(r.text)[3];
df.set_index(df.columns[0], {
  "inplace": true
});
df.index.rename("\uc8fc\uc694\uc7ac\ubb34\uc815\ubcf4", {
  "inplace": true
});
df.columns = df.columns.droplevel(2);
annual_date = new pd.DataFrame(df).xs("\ucd5c\uadfc \uc5f0\uac04 \uc2e4\uc801", {
  "axis": 1
});
quater_date = new pd.DataFrame(df).xs("\ucd5c\uadfc \ubd84\uae30 \uc2e4\uc801", {
  "axis": 1
});
