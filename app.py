from flask import Flask, render_template, request
import os  # For file existence checks

app = Flask(__name__)

# Stream data (hardcoded) - unchanged
streams = {
    'bio_maths': {
        'name': 'Bio-Maths Group',
        'description': 'Biology + Mathematics for Medical and Engineering fields',
        'subjects': ['Biology', 'Mathematics', 'Physics', 'Chemistry'],
        'careers': ['Medical Doctor', 'Engineer', 'Research Scientist', 'Biotechnologist'],
        'min_marks': 60
    },
    'pure_science': {
        'name': 'Pure Science Group',
        'description': 'Physics, Chemistry, Mathematics for Engineering and Pure Sciences',
        'subjects': ['Physics', 'Chemistry', 'Mathematics', 'Computer Science'],
        'careers': ['Engineer', 'Scientist', 'Researcher', 'Data Analyst'],
        'min_marks': 70
    },
    'commerce': {
        'name': 'Commerce Group',
        'description': 'Commerce with Accounts, Business Studies and Economics',
        'subjects': ['Accountancy', 'Business Studies', 'Economics', 'Mathematics'],
        'careers': ['Chartered Accountant', 'Company Secretary', 'Business Manager', 'Banker'],
        'min_marks': 55
    }
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/tenth.html', methods=['GET', 'POST'])
def tenth():
    if request.method == 'POST':
        try:
            maths_interest = int(request.form.get('maths_interest', 0))
            science_interest = int(request.form.get('science_interest', 0))
            bio_interest = int(request.form.get('bio_interest', 0))
            commerce_interest = int(request.form.get('commerce_interest', 0))
            current_marks = int(request.form.get('current_marks', 0))

            if maths_interest >= 4 and science_interest >= 4 and bio_interest >= 4 and current_marks >= 70:
                recommended = 'bio_maths'
            elif maths_interest >= 4 and science_interest >= 4 and current_marks >= 65:
                recommended = 'pure_science'
            elif commerce_interest >= 4 and current_marks >= 55:
                recommended = 'commerce'
            else:
                scores = {
                    'bio_maths': (maths_interest + science_interest + bio_interest) / 3,
                    'pure_science': (maths_interest + science_interest) / 2,
                    'commerce': commerce_interest
                }
                max_score = max(scores.values())
                if max_score == scores['bio_maths'] and current_marks >= 60:
                    recommended = 'bio_maths'
                elif max_score == scores['pure_science'] and current_marks >= 65:
                    recommended = 'pure_science'
                elif max_score == scores['commerce'] and current_marks >= 55:
                    recommended = 'commerce'
                else:
                    recommended = 'Need improvement in marks for preferred stream'

            stream_info = streams.get(recommended, {}) if recommended in streams else {}
            return render_template('tenth.html', recommended=recommended, stream_info=stream_info)
        except ValueError:
            # Handle invalid input (e.g., non-numeric marks)
            return render_template('tenth.html', error="Please enter valid numbers for interests and marks.")

    return render_template('tenth.html')

@app.route('/twelfth.html', methods=['GET', 'POST'])
def twelfth():
    if request.method == 'POST':
        try:
            physics = int(request.form.get('physics', 0))
            chemistry = int(request.form.get('chemistry', 0))
            maths = int(request.form.get('maths', 0))
            biology = int(request.form.get('biology', 0))
            english = int(request.form.get('english', 0))

            total = physics + chemistry + maths + biology + english
            pcm_total = physics + chemistry + maths
            pcb_total = physics + chemistry + biology

            departments = []
            if pcm_total >= 240 and maths >= 75 and physics >= 70:
                departments.append('Engineering (B.Tech/B.E.)')
            if pcb_total >= 240 and biology >= 75 and chemistry >= 70:
                departments.append('Medical (MBBS/BDS)')
            if pcm_total >= 210 or pcb_total >= 210:
                departments.append('B.Sc. Pure Sciences')
            if maths >= 60 and total >= 350:
                departments.append('B.Com Commerce')
                departments.append('Business Administration')
            if total >= 300:
                departments.append('Arts and Humanities')
                departments.append('Social Sciences')

            return render_template('twelfth.html', departments=departments)
        except ValueError:
            return render_template('twelfth.html', error="Please enter valid numbers for marks.")

    return render_template('twelfth.html')

# Custom static file route for debugging (logs requests)
@app.route('/static/<path:filename>')
def send_static(filename):
    file_path = os.path.join(app.static_folder, filename)
    if os.path.exists(file_path):
        print(f"✅ Static file served: {filename} (exists: {os.path.getsize(file_path)} bytes)")
        return app.send_static_file(filename)
    else:
        print(f"❌ 404 Static file NOT FOUND: {filename} (path: {file_path})")
        # Optional: Return a placeholder response instead of 404
        return "File not found", 404

if __name__ == '__main__':
    print("🚀 Starting Flask app on http://0.0.0.0:8080")
    print("📁 Static folder:", app.static_folder)
    print("📂 Templates folder:", app.template_folder)
    app.run(host='0.0.0.0', port=8080, debug=True)
