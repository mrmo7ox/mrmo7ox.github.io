import os
import markdown
import glob
import json
import re
import shutil

def load_config(path="site.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[!] FATAL: {path} not found. The system cannot boot.")
        exit(1)

def init_directories(public_dir, assets_dir):
    os.makedirs(public_dir, exist_ok=True)
    os.makedirs(assets_dir, exist_ok=True)

def load_templates(template_dir):
    templates = {}
    for tmpl in ["base", "index", "category"]:
        with open(os.path.join(template_dir, f"{tmpl}.html"), "r", encoding="utf-8") as f:
            templates[tmpl] = f.read()
    return templates

def build_nav_bar(nav_items):
    nav_html = ""
    for item in nav_items:
        nav_html += f'<a href="{item["url"]}" class="hover:text-red-500 transition-colors">{item["label"]}</a>\n'
    return nav_html

def apply_globals(html_str, page_title, site_info, nav_html):
    html = html_str.replace("{{PAGE_TITLE}}", page_title)
    html = html.replace("{{SITE_TITLE}}", site_info.get("title", "Root System"))
    html = html.replace("{{NAV_BAR}}", nav_html)
    html = html.replace("{{FOOTER_TEXT}}", site_info.get("footer_text", ""))
    return html

def process_posts(content_dir, public_dir, templates, category_map, site_info, nav_html):
    """Parses markdown files, generates HTML posts, and groups them by category."""
    categories_data = {cat: [] for cat in category_map.keys()}
    md_files = glob.glob(os.path.join(content_dir, "*.md"))

    for file_path in md_files:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        if "---" not in raw_text:
            print(f"[!] Warning: No '---' separator found in {file_path}. Skipping file.")
            continue

        header_part, body_part = raw_text.split("---", 1)

        meta = {}
        for line in header_part.strip().split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                meta[key.strip()] = val.strip()

        title = meta.get("TITLE", "Untitled Node")
        category = meta.get("CATEGORY", "Uncategorized")
        date = meta.get("DATE", "")
        image = meta.get("IMAGE", "")
        
        filename = os.path.basename(file_path).replace(".md", ".html")

        html_content = markdown.markdown(body_part, extensions=['fenced_code', 'tables'])

        page_html = apply_globals(templates["base"], title, site_info, nav_html)
        
        post_header = f"<h1 class='text-4xl md:text-5xl font-bold mb-4 text-white uppercase tracking-tighter'>{title}</h1>"
        if date:
            post_header += f"<p class='text-red-600 font-bold mb-8 uppercase'>[ DATE: {date} ]</p>"
        if image:
            post_header += f"<img src='{image}' class='w-full h-64 md:h-96 object-cover border-4 border-white mb-8 grayscale contrast-125'>"
            
        post_body = f"{post_header}\n<div class='prose prose-invert prose-red max-w-none'>{html_content}</div>"
        page_html = page_html.replace("{{CONTENT}}", post_body)

        with open(os.path.join(public_dir, filename), "w", encoding="utf-8") as f:
            f.write(page_html)

        if category not in categories_data:
            categories_data[category] = []
        categories_data[category].append({
            'title': title, 
            'link': filename, 
            'image': image, 
            'date': date
        })

    return categories_data

def build_categories(categories_data, category_map, public_dir, templates, assets_config, site_info, nav_html):
    category_html_links = ""

    for cat_name, posts in categories_data.items():
        safe_name = re.sub(r'[^a-zA-Z0-9]', '_', cat_name.lower())
        cat_filename = f"cat_{safe_name}.html"
        
        post_list_html = ""
        if not posts:
            post_list_html = "<p class='text-gray-500 italic'>No system logs found for this sector yet.</p>"
        else:
            post_list_html += "<div class='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'>"
            for post in posts:
                img_src = post.get('image')
                if not img_src:
                    img_src = category_map.get(cat_name, "")
                
                img_tag = f"<img src='{img_src}' class='w-full h-full object-cover grayscale contrast-125 group-hover:grayscale-0 transition-all'>" if img_src else "<div class='w-full h-full bg-black flex items-center justify-center text-red-600 font-bold'>NO_IMG</div>"
                
                post_list_html += f"""
                <a href='{post['link']}' class='brutal-card block group overflow-hidden bg-black hover:border-red-600 transition-colors flex flex-col h-full'>
                    <div class='h-48 border-b-2 border-white group-hover:border-red-600 transition-colors overflow-hidden'>
                        {img_tag}
                    </div>
                    <div class='p-4 flex-grow flex flex-col justify-between'>
                        <h4 class='text-lg font-bold uppercase text-white group-hover:text-red-600 mb-4'>{post['title']}</h4>
                        <div class='flex justify-between items-end border-t-2 border-dashed border-gray-800 pt-2'>
                            <span class='text-xs text-gray-500 font-bold'>[ Read_Log ]</span>
                            <span class='text-xs text-red-600 font-bold'>{post.get('date', '')}</span>
                        </div>
                    </div>
                </a>
                """
            post_list_html += "</div>"
        
        cat_page = templates["category"].replace("{{CATEGORY_NAME}}", cat_name)
        cat_page = cat_page.replace("{{POST_LIST}}", post_list_html)
        
        final_cat_html = apply_globals(templates["base"], cat_name, site_info, nav_html)
        final_cat_html = final_cat_html.replace("{{CONTENT}}", cat_page)
        
        with open(os.path.join(public_dir, cat_filename), "w", encoding="utf-8") as f:
            f.write(final_cat_html)
            
        bg_value = category_map.get(cat_name, assets_config.get("default_category_bg", "#000000"))
        
        if bg_value.startswith(("./", "/", "assets", "http")):
            image_style = f"background-image: url('{bg_value}'); background-size: cover; background-position: center;"
        else:
            image_style = f"background-color: {bg_value};"
            
        category_html_links += f"""
        <a href="{cat_filename}" class="brutal-card h-64 relative flex items-center justify-center overflow-hidden group">
            <div class="absolute inset-0 grayscale contrast-125 opacity-40 group-hover:opacity-80 transition-opacity duration-300" style="{image_style}"></div>
            <div class="absolute inset-0 bg-black bg-opacity-50 group-hover:bg-opacity-0 transition-all duration-300"></div>
            <div class="relative z-10 bg-black border-2 border-red-600 px-4 py-2">
                <h3 class="text-2xl font-bold uppercase text-white group-hover:text-red-500">{cat_name} [{len(posts)}]</h3>
            </div>
        </a>
        """
    return category_html_links

def build_whoami(whoami_data, public_dir, templates, site_info, nav_html):
    if not whoami_data:
        return

    ctf_html = ""
    for ctf in whoami_data.get("ctf_placements", []):
        ctf_html += f"""
        <div class="brutal-card p-4 flex justify-between items-center mb-4 bg-black group hover:border-red-600 transition-colors">
            <!-- Left Side: Image and Details -->
            <div class="flex items-center gap-4">
                <img src="{ctf.get('image', '')}" class="w-16 h-16 grayscale border border-gray-700 object-cover group-hover:grayscale-0 transition-all">
                <div>
                    <h4 class="text-lg font-bold uppercase text-white group-hover:text-red-600 transition-colors">{ctf.get('event', 'Unknown Event')}</h4>
                    <p class="text-red-600 font-bold text-sm">{ctf.get('rank', 'Participant')}</p>
                </div>
            </div>
            
            <!-- Right Side: Massive Placement Number -->
            <div class="text-5xl md:text-6xl font-bold text-gray-800 group-hover:text-red-600 transition-colors pr-2 md:pr-6 tracking-tighter">
                {ctf.get('placement', '')}
            </div>
        </div>
        """

    skills_html = "".join([f"<span class='border-2 border-white px-2 py-1 text-sm m-1 inline-block'>{s}</span>" for s in whoami_data.get("skills", [])])

    projects_html = ""
    for project_group in whoami_data.get("projects", []):
        projects_html += f"<h3 class='text-2xl font-bold uppercase mt-10 mb-4 border-l-4 border-red-600 pl-3'>{project_group.get('category')}</h3>\n"
        projects_html += "<div class='grid grid-cols-1 md:grid-cols-2 gap-4'>"
        
        for item in project_group.get("items", []):
            project_url = item.get('url', '#')
            
            projects_html += f"""
            <div class="cursor-pointer brutal-card p-5 bg-black flex flex-col justify-between hover:border-red-600 transition-colors group">
                <div>
                    <div class="flex justify-between items-start mb-2">
                        <a href="{project_url}" target="_blank" class="text-xl font-bold text-white uppercase group-hover:text-red-600 transition-colors">
                            {item.get('name')} <span class="text-sm opacity-50 ml-1">↗</span>
                        </a>
                        <span class="bg-white text-black text-xs font-bold px-2 py-1 uppercase whitespace-nowrap ml-2">{item.get('lang')}</span>
                    </div>
                    <p class="text-gray-400 text-sm">{item.get('desc')}</p>
                </div>
            </div>
            """
        projects_html += "</div>"

    whoami_content = f"""
    <div class="max-w-4xl mx-auto">
        <h1 class="text-6xl font-bold uppercase mb-8 text-white tracking-tighter">Who Am I?</h1>
        <p class="text-xl text-gray-400 mb-12">{whoami_data.get('full_bio', '')}</p>
        
        <h2 class="text-3xl font-bold uppercase mb-6 text-red-600 border-b-2 border-red-600 pb-2">Competitive_History</h2>
        {ctf_html}
        
        <h2 class="text-3xl font-bold uppercase mt-16 mb-6 text-red-600 border-b-2 border-red-600 pb-2">Technical_Arsenal</h2>
        <div class="flex flex-wrap mb-12">{skills_html}</div>
        
        <h2 class="text-3xl font-bold uppercase mt-16 mb-6 text-red-600 border-b-2 border-red-600 pb-2">System_Archives // Projects</h2>
        <p class="text-gray-400 mb-6">A structured log of my exploits, system builds, and tools.</p>
        {projects_html}
        
        <h2 class="text-3xl font-bold uppercase mt-16 mb-6 text-red-600 border-b-2 border-red-600 pb-2">Credentials</h2>
        <p class="text-gray-400">{" // ".join(whoami_data.get('certifications', []))}</p>
    </div>
    """

    final_whoami = apply_globals(templates["base"], "Whoami", site_info, nav_html)
    final_whoami = final_whoami.replace("{{CONTENT}}", whoami_content)

    with open(os.path.join(public_dir, "whoami.html"), "w", encoding="utf-8") as f:
        f.write(final_whoami)

def build_index(category_html_links, public_dir, templates, site_info, assets_config, nav_html):
    index_content = templates["index"].replace("{{CATEGORIES}}", category_html_links)

    index_content = index_content.replace("{{PROFILE_PICTURE}}", assets_config.get("profile_picture", ""))
    index_content = index_content.replace("{{AUTHOR_NAME}}", site_info.get("author_name", "Author"))
    index_content = index_content.replace("{{STATUS_BADGE}}", site_info.get("status_badge", "Active"))
    index_content = index_content.replace("{{BIO_DESCRIPTION}}", site_info.get("bio_description", ""))

    final_index = apply_globals(templates["base"], "Home", site_info, nav_html)
    final_index = final_index.replace("{{CONTENT}}", index_content)

    with open(os.path.join(public_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(final_index)


def main():
    print("[*] Booting root system builder...")
    config = load_config()

    DIRS = config.get("directories", {})
    PUBLIC_DIR = DIRS.get("public", "public")
    CONTENT_DIR = DIRS.get("content", "content")
    TEMPLATE_DIR = DIRS.get("templates", "templates")
    ASSETS_DIR = os.path.join(PUBLIC_DIR, DIRS.get("assets", "assets"))

    init_directories(PUBLIC_DIR, ASSETS_DIR)

    print("[*] Migrating static assets...")
    if os.path.exists("assets"):
        shutil.copytree("assets", ASSETS_DIR, dirs_exist_ok=True)

    templates = load_templates(TEMPLATE_DIR)
    nav_html = build_nav_bar(config.get("navigation", []))
    site_info = config.get("site_info", {})

    print("[*] Compiling text nodes...")
    categories_data = process_posts(
        CONTENT_DIR, PUBLIC_DIR, templates, 
        config.get("category", {}), site_info, nav_html
    )

    print("[*] Generating category sectors...")
    category_links = build_categories(
        categories_data, config.get("category", {}), 
        PUBLIC_DIR, templates, config.get("assets", {}), 
        site_info, nav_html
    )

    print("[*] Building Whoami module...")
    build_whoami(config.get("whoami", {}), PUBLIC_DIR, templates, site_info, nav_html)

    print("[*] Assembling main interface...")
    build_index(category_links, PUBLIC_DIR, templates, site_info, config.get("assets", {}), nav_html)

    print("[+] System updated. Nodes compiled to /public successfully.")

if __name__ == "__main__":
    main()