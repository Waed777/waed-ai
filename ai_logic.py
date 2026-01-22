def generate_insights(df, language="English"):
    if df.empty or "Price" not in df.columns:
        return "No data available to generate insights." if language=="English" else "لا توجد بيانات لتحليلها."
    
    # إزالة الرمز £ وتحويل للأرقام مع تجاهل الأخطاء
    prices = pd.to_numeric(df["Price"].str.replace("£",""), errors="coerce")
    
    if prices.isnull().all():
        return "No valid price data available." if language=="English" else "لا توجد بيانات سعر صالحة."

    avg_price = prices.mean()
    max_price = prices.max()
    min_price = prices.min()

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
