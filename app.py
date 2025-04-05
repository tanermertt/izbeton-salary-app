import streamlit as st

# Sayfa başlığı
st.title("İzbeton A.Ş 2025 - Sözleşmenin İkinci Yılı Maaş Hesaplama Programı")

# Ay günleri
ay_gunleri = {
    "Ocak": 31, "Şubat": 28, "Mart": 31, "Nisan": 30, "Mayıs": 31, "Haziran": 30,
    "Temmuz": 31, "Ağustos": 31, "Eylül": 30, "Ekim": 31, "Kasım": 30, "Aralık": 31
}

# Kullanıcı Girdileri
ay = st.selectbox("Ay Seçimi:", list(ay_gunleri.keys()))
grup = st.selectbox("Grup:", ["A", "B", "C", "D"])
vardiya = st.selectbox("Vardiya Seçimi:", ["Tekli Vardiya", "İkili Vardiya", "Üçlü Vardiya"])
kidem_yili = st.slider("Kıdem Yılı (0-30):", 0, 30, 25)
imza_primi_yuzdesi = st.selectbox("Üretime Dayalı Risk Primi (%):", [0, 3, 4, 6])
calisan_gun = st.number_input("Çalışılan Günler:", min_value=0, max_value=31, value=20)
tatil_gun = st.number_input("Çalışılmayan Günler:", min_value=0, max_value=31, value=10)
yillik_izin = st.number_input("Yıllık İzin Gün Sayısı:", min_value=0, max_value=31, value=0)
fazla_mesai_saat = st.number_input("Fazla Mesai Saat:", min_value=0.0, value=0.0)
fazla_mesai_gun = st.number_input("Fazla Mesai Gün:", min_value=0, value=0)
gece_farki_saat = st.number_input("Gece Çalışması Saat:", min_value=0.0, value=0.0)
yol_yardimi = st.number_input("Ulaşım Yardımı (TL):", min_value=0.0, value=0.0)
ekstra_prim = st.number_input("Ekstra Prim (TL):", min_value=0.0, value=0.0)
ikramiye = st.number_input("İkramiye Gün Sayısı:", min_value=0.0, value=19.0)
isveren_bes_sigorta = st.number_input("İşveren Bireysel Emeklilik Katkısı (TL):", min_value=0.0, value=0.0)
evli = st.radio("Evli misiniz?", ["Evet", "Hayır"])
cocuk_sayisi = st.number_input("Çocuk Sayısı:", min_value=0, value=0 if evli == "Hayır" else 1)

# Hesapla butonu
if st.button("Maaşı Hesapla"):
    try:
        # Taban yevmiye ve zamlar
        taban_yevmiyeleri = {"A": 1731.59, "B": 1796.93, "C": 1877.90, "D": 1943.24}
        taban_yevmiyesi = taban_yevmiyeleri[grup]
        kidem_zammi = kidem_yili * 4.01
        imza_prim_miktar = taban_yevmiyesi * (imza_primi_yuzdesi / 100)
        son_yevmiyesi = taban_yevmiyesi + kidem_zammi + imza_prim_miktar

        toplam_gun = calisan_gun + tatil_gun
        main_kazanc = son_yevmiyesi * toplam_gun

        fazla_mesai_ucreti = (fazla_mesai_saat * (son_yevmiyesi / 7.5) * 2) + (fazla_mesai_gun * son_yevmiyesi * 2)
        gece_farki = (son_yevmiyesi / 7.5 * 2 / 2 * 0.2 * gece_farki_saat)

        if vardiya == "Tekli Vardiya":
            uretim_destek_primi = (taban_yevmiyesi * ay_gunleri[ay] / 100) * 7
        elif vardiya == "İkili Vardiya":
            uretim_destek_primi = (taban_yevmiyesi * ay_gunleri[ay] / 100) * 10
        else:
            uretim_destek_primi = (taban_yevmiyesi * ay_gunleri[ay] / 100) * 12

        # Sabit yardımlar
        aile_yardimi = 2301.54 if evli == "Evet" else 0
        cocuk_yardimi = cocuk_sayisi * 253.14
        yemek_yardimi = calisan_gun * 330.98
        sosyal_yardim = 3846.71
        sorumluluk_zammi = 6525.78
        yakacak_yardimi = 3309.77
        is_guclugu_primi = calisan_gun * 27.56
        ise_devam_tesvik_primi = (taban_yevmiyesi + kidem_zammi + imza_prim_miktar) * 2
        yillik_izin_kazanci = yillik_izin * (son_yevmiyesi * 0.35)
        brüt_ikramiye = son_yevmiyesi * ikramiye
        sendika_aidati = son_yevmiyesi

        # Toplamlar
        kazanclar_toplam = main_kazanc + fazla_mesai_ucreti + gece_farki
        yardimlar = (
            sorumluluk_zammi + yakacak_yardimi + is_guclugu_primi + aile_yardimi + cocuk_yardimi +
            yemek_yardimi + sosyal_yardim + ise_devam_tesvik_primi + ekstra_prim + brüt_ikramiye +
            uretim_destek_primi + yillik_izin_kazanci + yol_yardimi
        )
        toplam_brut = kazanclar_toplam + yardimlar

        sgk_matrah = toplam_brut - (aile_yardimi + cocuk_yardimi + yol_yardimi + (calisan_gun * 158))
        sgk_primi = sgk_matrah * 0.14
        issizlik_primi = sgk_matrah * 0.01

        gelir_vergisi_matrahi = toplam_brut - (sgk_primi + issizlik_primi + yol_yardimi +
                                                cocuk_yardimi + sendika_aidati + isveren_bes_sigorta + (calisan_gun * 240))
        gelir_vergisi_matrahi = max(gelir_vergisi_matrahi, 0)

        if ay in ["Ocak", "Şubat"]:
            vergi_orani = 0.15
        elif ay in ["Mart", "Nisan"]:
            vergi_orani = 0.20
        elif ay in ["Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım"]:
            vergi_orani = 0.27
        else:
            vergi_orani = 0.35

        if ay in ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran"]:
            istisna = 3315.60
        elif ay == "Temmuz":
            istisna = 4257.57
        else:
            istisna = 4420.80

        toplam_vergi = (gelir_vergisi_matrahi * vergi_orani) - istisna
        damga_vergisi = (toplam_brut * 0.00759) - 197.38
        damga_vergisi = max(damga_vergisi, 0)

        net_maas = toplam_brut - (sgk_primi + issizlik_primi + toplam_vergi + damga_vergisi + sendika_aidati + yol_yardimi)

        # Sonuçları göster
        st.success(f"💰 Bankaya Yatan Net Maaş: **{net_maas:,.2f} TL**")
        st.write("---")
        st.subheader("📊 Detaylar")
        st.write(f"Toplam Brüt Maaş: {toplam_brut:,.2f} TL")
        st.write(f"SGK Matrahı: {sgk_matrah:,.2f} TL")
        st.write(f"Gelir Vergisi Matrahı: {gelir_vergisi_matrahi:,.2f} TL")
        st.write(f"Toplam Vergi: {toplam_vergi:,.2f} TL")
        st.write(f"Damga Vergisi: {damga_vergisi:,.2f} TL")

    except Exception as e:
        st.error(f"Hata oluştu: {e}")
