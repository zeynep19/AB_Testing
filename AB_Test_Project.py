########################################################################################
# AB Test Project
########################################################################################
# Business Problem: Facebook recently introduced a new type of bidding, average bidding,
# as an alternative to the current type of bidding called maximum bidding. One of our clients,
# bombabomba.com, decided to test this new feature and wants to do an A/B test to see
# if averagebidding converts more than maximumbidding.
# Maximum Bidding: Maksimum teklif verme
# Average Bidding: Average teklif verme
########################################################################################
# Dataset Story: In this data set, which contains the website information of bombabomba.com,
# there is information such as the number of advertisements that users see and click,
# as well as earnings information from here.
# There are two separate data sets, the control and test groups.
########################################################################################
# Variables:
# Impression – Ad views
# Click – Click (Indicates the number of clicks on the displayed ad.)
# Purchase – Indicates the number of products purchased after the clicked ads.
# Earning – Earnings after purchased items
########################################################################################

import pandas as pd
from scipy.stats import shapiro, levene, ttest_ind
from matplotlib import pyplot

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

########################################################################################
# AB Testing (Bağımsız İki Örneklem T Testi)

# İki grup ortalaması arasında karşılaştırma yapılmak istenildiğinde kullanılır.

# 1. Varsayım Kontrolü
#   - 1. Normallik Varsayımı
#   - 2. Varyans Homojenliği
# 2. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)
# Not:
# - Normallik sağlanmıyorsa direk 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.
########################################################################################

df_max = pd.read_excel("pythonProject/datasets/ab_testing.xlsx", sheet_name="Control Group")
df_avr = pd.read_excel("pythonProject/datasets/ab_testing.xlsx", sheet_name="Test Group")
df_max.head()
df_avr.head()

# Test ve Control grubunun purchase dağılımı
pyplot.figure(figsize=(8,6))
pyplot.xlabel("Purchase")
pyplot.hist(df_max["Purchase"],bins=15, alpha=0.7, label="Control Group")
pyplot.hist(df_avr["Purchase"],bins=15, alpha=0.7, label="Test Group")
pyplot.legend(loc="upper right")
pyplot.show()

# Kontrol ve test grubunun birleştirilmesi
df_max["Group"] = "A" # Maximum Bidding
df_avr["Group"] = "B" # Average Bidding
AB = df_max.append(df_avr) #AB testi için AB değişkeni
AB.head()

# Kontrol ve Test gruplarının purchase ortalamaları
print(" Mean of purchase of control group: %.3f" %AB[AB["Group"]== "A"]["Purchase"].mean(),"\n",
"Mean of purchase of test group: %.3f" %AB[AB["Group"]== "B"]["Purchase"].mean())
# Mean of purchase of control group: 550.894
# Mean of purchase of test group: 582.106

# Görev 1: A/B testinin hipotezini tanımlayınız.

# H0: "averagebidding(B) ile maximumbidding(A) arasında istatiksel olarak anlamlı fark yoktur." (M1 = M2)
# H1: "averagebidding(B) ile maximumbidding(A) arasında istatiksel olarak anlamlı fark vardır." (M1 != M2)

# Varsayım Kontrolü:
#   Normallik Varsayımı
#   Varyans Homojenliği

# Normallik Varsayımı
# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: Normal dağılım varsayımı sağlanmamaktadır.

# p-value < ise 0.05'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.

test_stat, pvalue = shapiro(AB.loc[AB["Group"] == "A", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 0.9773, p-value = 0.5891 --> H0 reddedilemez

test_stat, pvalue = shapiro(AB.loc[AB["Group"] == "B", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 0.9589, p-value = 0.1541 --> H0 reddedilemez

# varsayım sağlandı.

# Varyans Homojenligi Varsayımı

# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.

test_stat, pvalue = levene(AB.loc[AB["Group"] == "A", "Purchase"],
                           AB.loc[AB["Group"] == "B", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 2.6393, p-value = 0.1083 --> H0 reddedilemez

# Varsayımlar sağlandı, bağımsız iki örneklem t testi (parametrik test)

# Hipotezin Uygulanması

# H0: "averagebidding(B) ile maximumbidding(A) arasında istatiksel olarak anlamlı fark yoktur." (M1 = M2)
# H1: "averagebidding(B) ile maximumbidding(A) arasında istatiksel olarak anlamlı fark vardır." (M1 != M2)


# Bağımsız iki örneklem t testi (parametrik test)

test_stat, pvalue = ttest_ind(AB.loc[AB["Group"] == "A", "Purchase"],
                              AB.loc[AB["Group"] == "B", "Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = -0.9416, p-value = 0.3493 --> H0 reddedilemez

# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.

# Görev 2: Çıkan test sonuçlarının istatistiksel olarak anlamlı olup olmadığını yorumlayınız.
# p > 0.05 yani "averagebidding(B) ile maximumbidding(A) arasında istatiksel olarak anlamlı fark yoktur."
# Satın almada bir fark olmadığı yani yeni önerinin daha fazla satın alma getirmediği A/B testi ile kanıtlandı.

# Görev 3: Hangi testleri kullandınız? Sebeplerini belirtiniz.
# AB Testing (Bağımsız İki Örneklem T Testi), iki grup ortalaması arasında karşılaştırma yapılmak istenildiğinde kullanılır.
# Bağımsız iki örneklem T testinin (AB Testi) uygulanabilmesi için Normal dağılım ve Varyans homojenliği varsayımlarının
# sağlanması gerekir.
# 1. Normallik Varsayımı, kontrol etmek için Shapiro Wilk testi kullanılır.
# 2. Varyans Homojenliği, Levene testi kullanılarak değerlendirilir.
# Hipotezin Uygulanması: varsayımlar sağlandığı için bağımsız iki örneklem t testi (parametrik test) uygulandı.

# Görev 4: Görev 2’de verdiğiniz cevaba göre, müşteriye tavsiyeniz nedir?
# İki özellik arasında satın almada istatiksel olarak anlamlı fark yok fakat
# Tıklama Oranı(CTR-Reklam tıklanma sayısı (Click) / Reklam izlenme sayısı (Impression)) ile kullanıcıların
# reklamı ne kadar çok tıkladıklarına bakılıp tıklamalara göre satışlarda zamanla artma gözlenebilir.
