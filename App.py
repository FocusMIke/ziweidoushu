# -*- coding: utf-8 -*-
import streamlit as st
import datetime
from zhdate import ZhDate # 用于公历转农历

# =====================================================================================
# ===================== 核心演算代码区 (源于您的脚本) =====================
# =====================================================================================

# 核心数据定义
HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
PALACE_NAMES = ["命宫", "兄弟宫", "夫妻宫", "子女宫", "财帛宫", "疾厄宫", "迁移宫", "仆役宫", "事业宫", "田宅宫", "福德宫", "父母宫"]

# 十天干四化表 (及其他核心数据)
HUA_LU = {"甲": "廉贞", "乙": "天机", "丙": "天同", "丁": "太阴", "戊": "贪狼", "己": "武曲", "庚": "太阳", "辛": "巨门", "壬": "天梁", "癸": "破军"}
HUA_QUAN = {"甲": "破军", "乙": "天梁", "丙": "天机", "丁": "天同", "戊": "太阴", "己": "贪狼", "庚": "武曲", "辛": "太阳", "壬": "紫微", "癸": "巨门"}
HUA_KE = {"甲": "武曲", "乙": "紫微", "丙": "文昌", "丁": "天机", "戊": "右弼", "己": "天梁", "庚": "太阴", "辛": "文曲", "壬": "左辅", "癸": "太阴"}
HUA_JI = {"甲": "太阳", "乙": "太阴", "丙": "廉贞", "丁": "巨门", "戊": "天机", "己": "文曲", "庚": "天同", "辛": "文昌", "壬": "武曲", "癸": "贪狼"}
ZIWEI_GROUP = {"紫微": 0, "天机": -1, "太阳": -3, "武曲": -4, "天同": -5, "廉贞": -8}
TIANFU_GROUP = {"天府": 0, "太阴": 1, "贪狼": 2, "巨门": 3, "天相": 4, "天梁": 5, "七杀": 6, "破军": 10}

def get_ganzhi_of_year(year):
    """根据公历年份计算当年的天干地支"""
    stem_index = (year - 4) % 10
    branch_index = (year - 4) % 12
    return HEAVENLY_STEMS[stem_index] + EARTHLY_BRANCHES[branch_index]

def get_ganzhi_of_date(target_date):
    """根据公历日期计算当天的天干地支"""
    ref_date = datetime.date(2000, 1, 1)
    ref_stem_index = 6 # 庚
    ref_branch_index = 4 # 辰
    days_diff = (target_date - ref_date).days
    target_stem_index = (ref_stem_index + days_diff % 10 + 10) % 10
    target_branch_index = (ref_branch_index + days_diff % 12 + 12) % 12
    return HEAVENLY_STEMS[target_stem_index] + EARTHLY_BRANCHES[target_branch_index]

def format_lunar_month(month_int):
    """将农历月份数字转为中文"""
    months = ["正月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "冬月", "腊月"]
    return months[month_int-1]

def format_lunar_day(day_int):
    """将农历日期数字转为中文"""
    if day_int <= 10: return "初" + "一二三四五六七八九十"[day_int-1]
    elif day_int < 20: return "十" + "一二三四五六七八九"[day_int-11]
    elif day_int == 20: return "二十"
    elif day_int < 30: return "廿" + "一二三四五六七八九"[day_int-21]
    elif day_int == 30: return "三十"
    return ""

class NatalChart:
    def __init__(self, year, month, day, hour):
        self.star_pos_idx, self.palace_pos_idx = {}, {}
        self.natal_hua_ji_idx = -1
        
        year_gan = get_ganzhi_of_year(year)[0]
        birth_info = ZhDate(year, month, day)
        lunar_month, lunar_day = birth_info.lunar_month, birth_info.lunar_day
        
        self._calculate_chart(year_gan, lunar_month, lunar_day, hour)
        self.year_gan = year_gan

    def _calculate_chart(self, year_gan, lunar_month, lunar_day, hour):
        # 内部逻辑与您的脚本完全相同
        hour_zhi_idx = (hour + 1) // 2 % 12 if hour != 23 else 0
        ming_gong_idx = (lunar_month - 1 - hour_zhi_idx + 12) % 12
        self.palace_pos_idx["命宫"] = ming_gong_idx
        for i in range(12): self.palace_pos_idx[PALACE_NAMES[i]] = (ming_gong_idx - i + 12) % 12
        ming_gong_ganzhi_stem_idx = (HEAVENLY_STEMS.index(year_gan) % 5 * 2 + ming_gong_idx) % 10
        ming_gong_ganzhi = HEAVENLY_STEMS[ming_gong_ganzhi_stem_idx] + EARTHLY_BRANCHES[ming_gong_idx]
        ju_map = {"甲子":4,"乙丑":4,"丙寅":3,"丁卯":3,"戊辰":5,"己巳":5,"庚午":6,"辛未":6,"壬申":2,"癸酉":2,"甲戌":4,"乙亥":4,"丙子":2,"丁丑":2,"戊寅":6,"己卯":6,"庚辰":4,"辛巳":4,"壬午":5,"癸未":5,"甲申":3,"乙酉":3,"丙戌":6,"丁亥":6,"戊子":6,"己丑":6,"庚寅":5,"辛卯":5,"壬辰":2,"癸巳":2,"甲午":4,"乙未":4,"丙申":6,"丁酉":6,"戊戌":5,"己亥":5,"庚子":5,"辛丑":5,"壬寅":4,"癸卯":4,"甲辰":6,"乙巳":6,"丙午":2,"丁未":2,"戊申":5,"己酉":5,"庚戌":4,"辛亥":4,"壬子":3,"癸丑":3,"甲寅":2,"乙卯":2,"丙辰":5,"丁巳":5,"戊午":6,"己未":6,"庚申":3,"辛酉":3,"壬戌":2,"癸亥":2}
        wu_xing_ju = ju_map[ming_gong_ganzhi]
        shang, yushu = divmod(lunar_day, wu_xing_ju)
        if yushu == 0: shang -=1; yushu = wu_xing_ju
        temp_list = [2,1,4,3,6,5]
        temp = temp_list[wu_xing_ju-1]
        ziwei_idx = (ming_gong_idx + shang * (1 if ming_gong_idx in [0,1,6,7] else -1) + (yushu - 1) * (1 if ming_gong_idx in [2,3,4,5,8,9,10,11] else -1) + 12) %12
        ziwei_idx_map = { 2: [2, 1, 4, 3, 6, 5], 3: [1, 5, 2, 6, 3, 4], 4: [3, 2, 6, 5, 1, 4], 5: [4, 3, 1, 6, 2, 5], 6: [5, 4, 3, 2, 1, 6] }
        ziwei_idx = ziwei_idx_map[wu_xing_ju][(lunar_day + wu_xing_ju-1) // wu_xing_ju -1] if ming_gong_idx in [0,6] else \
                ziwei_idx_map[wu_xing_ju][(lunar_day + wu_xing_ju-1) // wu_xing_ju ]-1 if ming_gong_idx in [1,7] else \
                (ming_gong_idx + ( (lunar_day-1)//wu_xing_ju) * (1 if ming_gong_idx in [2,3,4,5] else -1) + 12)%12

        for star, offset in ZIWEI_GROUP.items(): self.star_pos_idx[star] = (ziwei_idx + offset + 12) % 12
        tianfu_idx = (5 - ziwei_idx + 12) % 12
        for star, offset in TIANFU_GROUP.items(): self.star_pos_idx[star] = (tianfu_idx + offset) % 12
        self.star_pos_idx["左辅"], self.star_pos_idx["右弼"] = (lunar_month-1+2)%12, (11-(lunar_month-1))%12
        self.star_pos_idx["文昌"], self.star_pos_idx["文曲"] = (10-hour_zhi_idx+12)%12, (4+hour_zhi_idx)%12
        natal_ji_star = HUA_JI.get(year_gan)
        self.natal_hua_ji_idx = self.star_pos_idx.get(natal_ji_star, -1)

    def _get_branch_name(self, index):
        return EARTHLY_BRANCHES[index] if 0 <= index < 12 else "未知"

    def analyze_day(self, daily_stem):
        # 计分逻辑与您的脚本完全相同
        lu_star, quan_star, ke_star, ji_star = HUA_LU.get(daily_stem), HUA_QUAN.get(daily_stem), HUA_KE.get(daily_stem), HUA_JI.get(daily_stem)
        lu_pos_idx, quan_pos_idx, ke_pos_idx, ji_pos_idx = self.star_pos_idx.get(lu_star, -1), self.star_pos_idx.get(quan_star, -1), self.star_pos_idx.get(ke_star, -1), self.star_pos_idx.get(ji_star, -1)
        score, analysis_log = 0, []
        if lu_pos_idx != -1:
            if lu_pos_idx == self.palace_pos_idx.get("财帛宫"): score += 1; analysis_log.append(f"  • [吉+1] 流日化禄 ({lu_star}禄) 进入本命财帛宫 (在{self._get_branch_name(lu_pos_idx)}宫)，主今日有直接的财务机遇或进账。")
            if lu_pos_idx == self.palace_pos_idx.get("福德宫"): score += 1; analysis_log.append(f"  • [吉+1] 流日化禄 ({lu_star}禄) 进入本命福德宫 (在{self._get_branch_name(lu_pos_idx)}宫)，主今日心态愉悦，直觉敏锐，利于投机和决策。")
            if lu_pos_idx == self.palace_pos_idx.get("命宫"): score += 1; analysis_log.append(f"  • [吉+1] 流日化禄 ({lu_star}禄) 进入本命命宫 (在{self._get_branch_name(lu_pos_idx)}宫)，主今日整体运势顺遂，心情佳，人缘好。")
        if quan_pos_idx != -1 and (quan_pos_idx == self.palace_pos_idx.get("财帛宫") or quan_pos_idx == self.palace_pos_idx.get("命宫")): score += 1; analysis_log.append(f"  • [吉+1] 流日化权 ({quan_star}权) 进入关键宫位 (在{self._get_branch_name(quan_pos_idx)}宫)，主今日决策果断，掌控力强，利于主动出击。")
        if ji_pos_idx != -1:
            clashed_by_ji_idx = (ji_pos_idx + 6) % 12
            clashed_palace_name = self._get_branch_name(clashed_by_ji_idx)
            if clashed_by_ji_idx == self.natal_hua_ji_idx and self.natal_hua_ji_idx != -1: score = -2; analysis_log.append(f"  • [!!!最大风险!!!] 流日化忌 ({ji_star}忌) 在{self._get_branch_name(ji_pos_idx)}宫，猛烈冲击位于{clashed_palace_name}宫的生年化忌星。此为“冲起忌星”，是为大凶之兆，极易引爆命中固有隐患，应万事谨慎，规避风险！")
            else:
                if clashed_by_ji_idx == self.palace_pos_idx.get("财帛宫"): score -= 2; analysis_log.append(f"  • [大凶-2] 流日化忌 ({ji_star}忌) 直冲本命财帛宫 (在{clashed_palace_name}宫)，谨防因{self._get_branch_name(ji_pos_idx)}宫相关人事物引发的突然破财。")
                if clashed_by_ji_idx == self.palace_pos_idx.get("福德宫"): score -= 2; analysis_log.append(f"  • [大凶-2] 流日化忌 ({ji_star}忌) 直冲本命福德宫 (在{clashed_palace_name}宫)，心态极易失衡，判断力严重下降，绝不宜做任何投机决定。")
                if clashed_by_ji_idx == self.palace_pos_idx.get("命宫"): score -= 2; analysis_log.append(f"  • [大凶-2] 流日化忌 ({ji_star}忌) 直冲本命命宫 (在{clashed_palace_name}宫)，运势严重受阻，易感压力巨大，身心俱疲。")
            if ji_pos_idx == self.palace_pos_idx.get("财帛宫"): score -= 1; analysis_log.append(f"  • [凶-1] 流日化忌 ({ji_star}忌) 坐入本命财帛宫 (在{self._get_branch_name(ji_pos_idx)}宫)，主今日为财奔波烦恼，易有财务压力。")
            if ji_pos_idx == self.palace_pos_idx.get("福德宫"): score -= 1; analysis_log.append(f"  • [凶-1] 流日化忌 ({ji_star}忌) 坐入本命福德宫 (在{self._get_branch_name(ji_pos_idx)}宫)，主今日思绪混乱，内心不宁，易钻牛角尖。")
        final_score = max(-2, min(2, score))
        if not analysis_log: analysis_log.append("  • 今日无重大吉凶星象引动关键宫位，运势平稳。")
        interpretations = {2:"大吉",1:"吉",0:"平",-1:"凶",-2:"大凶"}; interpretation_details = {2:"机会极佳，果断出击",1:"运势顺利，可积极作为",0:"无明显吉凶，宜静观其变",-1:"诸事不宜，谨慎防守",-2:"风险极高，规避为上"}
        return {"transformations":{"禄":f"{lu_star} ({self._get_branch_name(lu_pos_idx)})","权":f"{quan_star} ({self._get_branch_name(quan_pos_idx)})","科":f"{ke_star} ({self._get_branch_name(ke_pos_idx)})","忌":f"{ji_star} ({self._get_branch_name(ji_pos_idx)})"}, "score":final_score, "interpretation":interpretations.get(final_score), "interpretation_details":interpretation_details.get(final_score), "analysis_log":"\n".join(analysis_log)}

# ===================================================================
# =================== Streamlit 用户界面与交互区 ===================
# ===================================================================

st.set_page_config(page_title="紫微斗数-日运分析", page_icon="🔮", layout="centered")

# --- 页面标题 ---
st.title("🔮 紫微斗数-日运分析")
st.caption("v6.2 - Streamlit Web App (终极可靠版)")

# --- 侧边栏用于输入生日信息 ---
with st.sidebar:
    st.header("👤 您的出生信息")
    st.info("请提供您的公历出生信息。所有信息仅用于本次计算，不会被储存或上传。")
    
    # 使用统一的日期选择器，更方便
    birth_date = st.date_input(
        "出生年月日 (公历)",
        value=datetime.date(1990, 10, 25),
        min_value=datetime.date(1924, 1, 1), # 甲子年开始
        max_value=datetime.date.today()
    )
    
    birth_hour = st.slider("出生时辰 (24小时制)", 0, 23, 8, help="0点代表子时，23点代表亥时末。")

# --- 主页面用于选择分析日期 ---
st.header("📅 您要分析的日期")
target_date = st.date_input("选择一个公历日期进行分析", datetime.date(2025, 10, 8))

# --- 分析按钮 ---
if st.button("🚀 开始分析", type="primary", use_container_width=True):
    with st.spinner('正在排盘和演算中，请稍候...'):
        try:
            # 从日期选择器中获取年月日
            birth_year = birth_date.year
            birth_month = birth_date.month
            birth_day = birth_date.day
            
            # 1. 初始化命盘
            my_chart = NatalChart(birth_year, birth_month, birth_day, birth_hour)
            
            # 2. 计算目标日干支
            target_date_ganzhi = get_ganzhi_of_date(target_date)
            
            # 3. 分析日运
            daily_luck = my_chart.analyze_day(target_date_ganzhi[0])

            # --- 结果展示 ---
            st.success("分析完成！")
            st.subheader(f"📊 {target_date.strftime('%Y-%m-%d')} 的日运分析报告")

            # 显示综合评级
            st.metric(
                label=f"综合评级: {daily_luck['interpretation']}",
                value=daily_luck['interpretation_details'],
                delta=f"分数: {daily_luck['score']}",
                delta_color="normal"
            )
            
            st.markdown("---")

            # 当日四化状态
            with st.expander("【点击查看当日四化状态】", expanded=True):
                cols = st.columns(4)
                hua_map = {"禄": "green", "权": "blue", "科": "orange", "忌": "red"}
                for i, (hua, star_info) in enumerate(daily_luck['transformations'].items()):
                    with cols[i]:
                        st.markdown(f"##### 化{hua}")
                        st.markdown(f"> <font color='{hua_map[hua]}'>{star_info}</font>", unsafe_allow_html=True)
            
            st.markdown("---")

            # 推演过程与建议
            st.subheader("【推演过程与建议】")
            st.info(daily_luck['analysis_log'])

            # 显示输入的生日信息以供核对
            with st.expander("【点击查看您的输入信息】"):
                birth_info_display = ZhDate(birth_year, birth_month, birth_day)
                lunar_year_str = birth_info_display.lunar_year
                lunar_month_str = format_lunar_month(birth_info_display.lunar_month)
                lunar_day_str = format_lunar_day(birth_info_display.lunar_day)

                st.write(f"**您输入的公历生日:** {birth_year}年{birth_month}月{birth_day}日 {birth_hour}时")
                st.write(f"**转换为农历:** {lunar_year_str}年 {lunar_month_str}{lunar_day_str}")
                st.write(f"**当年干支:** {get_ganzhi_of_year(birth_year)}")
                st.write(f"**分析日期干支:** {target_date_ganzhi}")

        except Exception as e:
            st.error(f"发生错误：{e}")
            st.warning("演算失败，请仔细检查您在左侧栏输入的生日信息是否准确无误。")
