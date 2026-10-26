import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle

def create_erd(theme="dark"):
    is_dark = (theme == "dark")
    bg_color = "#0f172a" if is_dark else "#ffffff"
    card_bg = "#1e293b" if is_dark else "#f8fafc"
    card_border_fallback = "#334155" if is_dark else "#cbd5e1"
    row_line_color = "#334155" if is_dark else "#e2e8f0"
    text_main = "#f8fafc" if is_dark else "#0f172a"
    text_muted = "#94a3b8" if is_dark else "#64748b"
    title_sub = "#38bdf8" if is_dark else "#0284c7"
    
    fig, ax = plt.subplots(figsize=(20, 13), dpi=300)
    ax.set_xlim(0, 2000)
    ax.set_ylim(0, 1300)
    ax.axis("off")
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    
    # Header
    ax.text(1000, 1260, "BITS College • Department of Software Engineering • SWEN466: Knowledge Discovery & Data Mining",
            ha="center", va="center", color=text_muted, fontsize=13, weight="bold", fontfamily="sans-serif")
    ax.text(1000, 1220, "Olist E-Commerce Entity-Relationship Diagram (Crow's Foot Notation)",
            ha="center", va="center", color=text_main, fontsize=22, weight="bold", fontfamily="sans-serif")
    ax.text(1000, 1185, "Primary Keys [PK], Foreign Keys [FK], Cardinalities & Relationship Verbs",
            ha="center", va="center", color=title_sub, fontsize=12, fontfamily="sans-serif")

    # Table styles
    if is_dark:
        colors = {
            "customers": {"header": "#1e3a8a", "border": "#3b82f6"},
            "orders": {"header": "#065f46", "border": "#10b981"},
            "order_items": {"header": "#831843", "border": "#ec4899"},
            "products": {"header": "#78350f", "border": "#f59e0b"},
            "sellers": {"header": "#4c1d95", "border": "#8b5cf6"}
        }
    else:
        colors = {
            "customers": {"header": "#2563eb", "border": "#1d4ed8"},
            "orders": {"header": "#059669", "border": "#047857"},
            "order_items": {"header": "#db2777", "border": "#be185d"},
            "products": {"header": "#d97706", "border": "#b45309"},
            "sellers": {"header": "#7c3aed", "border": "#6d28d9"}
        }

    entities = {
        "customers": {
            "title": "raw.customers",
            "subtitle": "Grain: 1 row per order customer account",
            "x": 60, "y": 720, "w": 360, "h": 320,
            "color_key": "customers",
            "columns": [
                ("customer_id", "VARCHAR", "PK", True),
                ("customer_unique_id", "VARCHAR", "Natural Key", False),
                ("customer_zip_code_prefix", "VARCHAR", "", False),
                ("customer_city", "VARCHAR", "", False),
                ("customer_state", "VARCHAR", "", False)
            ]
        },
        "orders": {
            "title": "raw.orders",
            "subtitle": "Grain: 1 row per purchase order",
            "x": 560, "y": 660, "w": 400, "h": 410,
            "color_key": "orders",
            "columns": [
                ("order_id", "VARCHAR", "PK", True),
                ("customer_id", "VARCHAR", "FK", False),
                ("order_status", "VARCHAR", "", False),
                ("order_purchase_timestamp", "TIMESTAMP", "", False),
                ("order_approved_at", "TIMESTAMP", "", False),
                ("order_delivered_carrier_date", "TIMESTAMP", "", False),
                ("order_delivered_customer_date", "TIMESTAMP", "", False),
                ("order_estimated_delivery_date", "TIMESTAMP", "", False)
            ]
        },
        "order_items": {
            "title": "raw.order_items (Junction Table)",
            "subtitle": "Grain: 1 row per item inside an order",
            "x": 1100, "y": 680, "w": 410, "h": 380,
            "color_key": "order_items",
            "columns": [
                ("order_id", "VARCHAR", "PK, FK", True),
                ("order_item_id", "INTEGER", "PK", True),
                ("product_id", "VARCHAR", "FK", False),
                ("seller_id", "VARCHAR", "FK", False),
                ("shipping_limit_date", "TIMESTAMP", "", False),
                ("price", "DOUBLE", "Measure", False),
                ("freight_value", "DOUBLE", "Measure", False)
            ]
        },
        "products": {
            "title": "raw.products",
            "subtitle": "Grain: 1 row per catalog product",
            "x": 1600, "y": 600, "w": 360, "h": 440,
            "color_key": "products",
            "columns": [
                ("product_id", "VARCHAR", "PK", True),
                ("product_category_name", "VARCHAR", "", False),
                ("product_name_lenght", "INTEGER", "", False),
                ("product_description_lenght", "INTEGER", "", False),
                ("product_photos_qty", "INTEGER", "", False),
                ("product_weight_g", "DOUBLE", "", False),
                ("product_length_cm", "DOUBLE", "", False),
                ("product_height_cm", "DOUBLE", "", False),
                ("product_width_cm", "DOUBLE", "", False)
            ]
        },
        "sellers": {
            "title": "raw.sellers",
            "subtitle": "Grain: 1 row per marketplace seller",
            "x": 1120, "y": 140, "w": 370, "h": 280,
            "color_key": "sellers",
            "columns": [
                ("seller_id", "VARCHAR", "PK", True),
                ("seller_zip_code_prefix", "VARCHAR", "", False),
                ("seller_city", "VARCHAR", "", False),
                ("seller_state", "VARCHAR", "", False)
            ]
        }
    }

    def draw_entity(ent):
        x, y, w, h = ent["x"], ent["y"], ent["w"], ent["h"]
        ck = colors[ent["color_key"]]
        
        body_patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=12",
                                    facecolor=card_bg, edgecolor=ck["border"], linewidth=2.2, zorder=2)
        ax.add_patch(body_patch)
        
        header_h = 58
        header_patch = FancyBboxPatch((x, y + h - header_h), w, header_h,
                                      boxstyle="round,pad=0,rounding_size=12",
                                      facecolor=ck["header"], edgecolor=ck["border"], linewidth=2.2, zorder=3)
        ax.add_patch(header_patch)
        
        square_bottom = patches.Rectangle((x, y + h - header_h), w, 15,
                                          facecolor=ck["header"], edgecolor="none", zorder=3)
        ax.add_patch(square_bottom)
        
        ax.text(x + w / 2, y + h - 22, ent["title"],
                ha="center", va="center", color="#ffffff", fontsize=13, weight="bold", zorder=4)
        ax.text(x + w / 2, y + h - 42, ent["subtitle"],
                ha="center", va="center", color="#e2e8f0" if not is_dark else "#cbd5e1", fontsize=8.5, style="italic", zorder=4)
        
        ax.plot([x, x + w], [y + h - header_h, y + h - header_h], color=ck["border"], lw=1.8, zorder=4)
        
        row_y = y + h - header_h - 22
        for col_name, col_type, tag, is_pk in ent["columns"]:
            if tag:
                badge_color = "#eab308" if "PK" in tag else ("#0284c7" if "FK" in tag else ("#64748b" if not is_dark else "#94a3b8"))
                badge_text_color = "#000000" if "PK" in tag else "#ffffff"
                badge_w = 44 if len(tag) <= 3 else (70 if len(tag) <= 7 else 82)
                badge_box = FancyBboxPatch((x + 10, row_y - 9), badge_w, 18,
                                           boxstyle="round,pad=0,rounding_size=4",
                                           facecolor=badge_color, edgecolor="none", zorder=4)
                ax.add_patch(badge_box)
                ax.text(x + 10 + badge_w / 2, row_y, tag,
                        ha="center", va="center", color=badge_text_color, fontsize=8, weight="bold", zorder=5)
                text_x = x + 18 + badge_w
            else:
                text_x = x + 16
                
            col_weight = "bold" if is_pk else "normal"
            col_color = ("#0f172a" if is_pk else "#334155") if not is_dark else ("#f8fafc" if is_pk else "#e2e8f0")
            ax.text(text_x, row_y, col_name, ha="left", va="center",
                    color=col_color, fontsize=10, weight=col_weight, fontfamily="monospace", zorder=4)
            
            ax.text(x + w - 14, row_y, col_type, ha="right", va="center",
                    color=text_muted, fontsize=8.5, fontfamily="monospace", zorder=4)
            
            ax.plot([x + 10, x + w - 10], [row_y - 14, row_y - 14], color=row_line_color, lw=0.6, zorder=3)
            row_y -= 34

    for ent in entities.values():
        draw_entity(ent)

    # 1. customers -> orders
    rel1_color = "#2563eb" if not is_dark else "#60a5fa"
    ax.plot([420, 560], [880, 880], color=rel1_color, lw=2.8, zorder=2)
    ax.plot([440, 440], [868, 892], color=rel1_color, lw=2.5, zorder=3)
    ax.plot([450, 450], [868, 892], color=rel1_color, lw=2.5, zorder=3)
    ax.plot([530, 530], [868, 892], color=rel1_color, lw=2.5, zorder=3)
    ax.plot([540, 540], [868, 892], color=rel1_color, lw=2.5, zorder=3)
    ax.text(490, 905, "places", ha="center", va="center", color=rel1_color, fontsize=10, weight="bold",
            bbox=dict(boxstyle="round,pad=0.3", fc=bg_color, ec=rel1_color, lw=1.2))
    ax.text(490, 860, "1 : 1 in data\n(exactly one)", ha="center", va="center", color=text_muted, fontsize=7.5)

    # 2. orders -> order_items
    rel2_color = "#db2777" if not is_dark else "#f472b6"
    ax.plot([960, 1100], [880, 880], color=rel2_color, lw=2.8, zorder=2)
    ax.plot([980, 980], [868, 892], color=rel2_color, lw=2.5, zorder=3)
    ax.plot([990, 990], [868, 892], color=rel2_color, lw=2.5, zorder=3)
    circle_c = Circle((1060, 880), 7, facecolor=bg_color, edgecolor=rel2_color, lw=2.2, zorder=4)
    ax.add_patch(circle_c)
    ax.plot([1067, 1098], [880, 894], color=rel2_color, lw=2.5, zorder=3)
    ax.plot([1067, 1098], [880, 880], color=rel2_color, lw=2.5, zorder=3)
    ax.plot([1067, 1098], [880, 866], color=rel2_color, lw=2.5, zorder=3)
    ax.text(1025, 915, "contains", ha="center", va="center", color=rel2_color, fontsize=10, weight="bold",
            bbox=dict(boxstyle="round,pad=0.3", fc=bg_color, ec=rel2_color, lw=1.2))
    ax.text(1025, 845, "1 : 0..N\n(775 orders have 0 items,\nmax 21 items)", ha="center", va="center", color=text_muted, fontsize=7.5)

    # 3. products -> order_items
    rel3_color = "#d97706" if not is_dark else "#fbbf24"
    ax.plot([1600, 1510], [880, 880], color=rel3_color, lw=2.8, zorder=2)
    ax.plot([1580, 1580], [868, 892], color=rel3_color, lw=2.5, zorder=3)
    ax.plot([1570, 1570], [868, 892], color=rel3_color, lw=2.5, zorder=3)
    circle_p = Circle((1545, 880), 7, facecolor=bg_color, edgecolor=rel3_color, lw=2.2, zorder=4)
    ax.add_patch(circle_p)
    ax.plot([1538, 1512], [880, 894], color=rel3_color, lw=2.5, zorder=3)
    ax.plot([1538, 1512], [880, 880], color=rel3_color, lw=2.5, zorder=3)
    ax.plot([1538, 1512], [880, 866], color=rel3_color, lw=2.5, zorder=3)
    ax.text(1555, 915, "ordered in", ha="center", va="center", color=rel3_color, fontsize=10, weight="bold",
            bbox=dict(boxstyle="round,pad=0.3", fc=bg_color, ec=rel3_color, lw=1.2))
    ax.text(1555, 845, "1 : 0..N\n(catalog optional,\nin data 1..527)", ha="center", va="center", color=text_muted, fontsize=7.5)

    # 4. sellers -> order_items
    rel4_color = "#7c3aed" if not is_dark else "#a78bfa"
    ax.plot([1305, 1305], [420, 680], color=rel4_color, lw=2.8, zorder=2)
    ax.plot([1293, 1317], [440, 440], color=rel4_color, lw=2.5, zorder=3)
    ax.plot([1293, 1317], [450, 450], color=rel4_color, lw=2.5, zorder=3)
    circle_s = Circle((1305, 640), 7, facecolor=bg_color, edgecolor=rel4_color, lw=2.2, zorder=4)
    ax.add_patch(circle_s)
    ax.plot([1305, 1291], [647, 678], color=rel4_color, lw=2.5, zorder=3)
    ax.plot([1305, 1305], [647, 678], color=rel4_color, lw=2.5, zorder=3)
    ax.plot([1305, 1319], [647, 678], color=rel4_color, lw=2.5, zorder=3)
    ax.text(1385, 550, "fulfills", ha="center", va="center", color=rel4_color, fontsize=10, weight="bold",
            bbox=dict(boxstyle="round,pad=0.3", fc=bg_color, ec=rel4_color, lw=1.2))
    ax.text(1385, 515, "1 : 0..N\n(marketplace optional,\nin data 1..2,033)", ha="center", va="center", color=text_muted, fontsize=7.5)

    # Junction table callout
    callout_bg = "#831843" if is_dark else "#fdf2f8"
    callout_ec = "#ec4899" if is_dark else "#db2777"
    callout_txt = "#fce7f3" if is_dark else "#9d174d"
    ax.text(1305, 695, "▲ M:N RESOLUTION ▲\norder_items resolves Many-to-Many\nbetween orders, products & sellers",
            ha="center", va="bottom", color=callout_txt, fontsize=8.5, weight="bold",
            bbox=dict(boxstyle="round,pad=0.4", fc=callout_bg, ec=callout_ec, lw=1.5, alpha=0.9))

    # Legend box
    legend_box = FancyBboxPatch((60, 50), 960, 380, boxstyle="round,pad=0,rounding_size=10",
                                facecolor=card_bg, edgecolor=card_border_fallback, lw=1.8, zorder=2)
    ax.add_patch(legend_box)

    ax.text(80, 400, "ERD Crow's Foot Notation & Integrity Validation Rules",
            ha="left", va="center", color=text_main, fontsize=12, weight="bold")

    # Legend symbols
    ax.plot([90, 150], [360, 360], color=rel1_color, lw=2.5)
    ax.plot([130, 130], [350, 370], color=rel1_color, lw=2.5)
    ax.plot([140, 140], [350, 370], color=rel1_color, lw=2.5)
    ax.text(170, 360, "Mandatory One (Exactly One): Minimum = 1, Maximum = 1", color=text_main, fontsize=9.5, va="center")

    ax.plot([90, 150], [320, 320], color=rel2_color, lw=2.5)
    c_leg = Circle((125, 320), 5.5, facecolor=bg_color, edgecolor=rel2_color, lw=2)
    ax.add_patch(c_leg)
    ax.plot([131, 150], [320, 330], color=rel2_color, lw=2.2)
    ax.plot([131, 150], [320, 320], color=rel2_color, lw=2.2)
    ax.plot([131, 150], [320, 310], color=rel2_color, lw=2.2)
    ax.text(170, 320, "Optional Many (Zero or Many): Minimum = 0, Maximum = Many", color=text_main, fontsize=9.5, va="center")

    ax.text(80, 275, "[PK] Primary Key: Uniquely identifies each record (count(*) = count(DISTINCT), 0 nulls).", color="#ca8a04" if not is_dark else "#fde047", fontsize=9, va="center", weight="semibold")
    ax.text(80, 250, "[FK] Foreign Key: References parent primary key (validated via ANTI JOIN = 0 orphans).", color="#0284c7" if not is_dark else "#7dd3fc", fontsize=9, va="center", weight="semibold")
    ax.text(80, 225, "Composite Key: order_items requires (order_id, order_item_id) as its composite primary key.", color=text_muted, fontsize=9, va="center")

    ax.plot([80, 990], [200, 200], color=row_line_color, lw=1)
    ax.text(80, 175, "Empirical Findings from SQL Data Quality Checks:", color=text_main, fontsize=10, weight="bold", va="center")
    ax.text(80, 150, "• 775 orders have zero order_items (unavailable/canceled orders) -> Justifies the circle (0..N) on orders -> order_items.", color=text_muted, fontsize=8.5, va="center")
    ax.text(80, 125, "• In the raw data, every product and seller has at least 1 order_item (min = 1) -> Data snapshot is stricter than catalog diagram (1..N vs 0..N).", color=text_muted, fontsize=8.5, va="center")
    ax.text(80, 100, "• customer_id is created per purchase transaction (1:1 with orders); customer_unique_id identifies the real recurring human.", color=text_muted, fontsize=8.5, va="center")
    ax.text(80, 75, "• Zero orphaned child records: 100% referential integrity across all child-to-parent foreign key relationships.", color=text_muted, fontsize=8.5, va="center")

    plt.tight_layout()
    suffix = "_light" if not is_dark else ""
    png_name = f"erd_diagram{suffix}.png"
    pdf_name = f"erd_diagram{suffix}.pdf"
    plt.savefig(png_name, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.savefig(pdf_name, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Generated {png_name} and {pdf_name}")

create_erd("dark")
create_erd("light")
