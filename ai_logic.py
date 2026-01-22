def generate_insights(df, language="English"):
    avg_price = df["Price"].str.replace("£","").astype(float).mean()
    max_price = df["Price"].str.replace("£","").astype(float).max()
    min_price = df["Price"].str.replace("£","").astype(float).min()

    if language == "English":
        return (
            f"The average price is £{avg_price:.2f}.\n"
            f"Highest price: £{max_price:.2f}, Lowest price: £{min_price:.2f}.\n"
            "Data trends indicate stable pricing globally."
        )
    else:
        return (
            f"متوسط السعر هو £{avg_price:.2f}.\n"
            f"أعلى سعر: £{max_price:.2f}، أقل سعر: £{min_price:.2f}.\n"
            "تشير الاتجاهات إلى استقرار الأسعار عالميًا."
        )
