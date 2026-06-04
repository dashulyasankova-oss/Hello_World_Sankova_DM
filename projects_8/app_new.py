from flask import Flask, render_template, jsonify, send_file
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import io

app = Flask(__name__)

DB_NAME = "student_task"
DB_USER = "postgres"
DB_PASSWORD = "student"
DB_HOST = "localhost"
DB_PORT = "5433"

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stat/mean')
def api_mean():
    try:
        query = "SELECT grade FROM grades"
        df = pd.read_sql(query, engine)
        result = float(df['grade'].mean())
        return jsonify({"status": "success", "value": result, "metric": "mean"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/stat/median')
def api_median():
    try:
        query = "SELECT grade FROM grades"
        df = pd.read_sql(query, engine)
        result = float(df['grade'].median())
        return jsonify({"status": "success", "value": result, "metric": "median"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/stat/total')
def api_total():
    try:
        query = "SELECT COUNT(*) as cnt FROM grades"
        df = pd.read_sql(query, engine)
        result = int(df['cnt'].iloc[0])
        return jsonify({"status": "success", "value": result, "metric": "total"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/stat/std')
def api_std():
    try:
        query = "SELECT grade FROM grades"
        df = pd.read_sql(query, engine)
        result = float(df['grade'].std())
        return jsonify({"status": "success", "value": result, "metric": "std"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/stat/max')
def api_max():
    try:
        query = "SELECT grade FROM grades"
        df = pd.read_sql(query, engine)
        result = float(df['grade'].max())
        return jsonify({"status": "success", "value": result, "metric": "max"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/chart/histogram')
def api_histogram():
    try:
        query = "SELECT grade FROM grades"
        df = pd.read_sql(query, engine)
        mean_val = df['grade'].mean()
        median_val = df['grade'].median()
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(df['grade'], bins=10, edgecolor='black', alpha=0.7, color='#2A9D8F')
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean = {mean_val:.2f}')
        ax.axvline(median_val, color='blue', linestyle='--', linewidth=2, label=f'Median = {median_val:.2f}')
        ax.set_xlabel('Grade')
        ax.set_ylabel('Count')
        ax.set_title('Grade Distribution')
        ax.legend()
        ax.grid(True, alpha=0.3)
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        print(f"Error: {e}")
        return "Error", 500

@app.route('/api/chart/courses')
def api_courses():
    try:
        query = """
            SELECT c.title as course_name, AVG(g.grade) as avg_grade
            FROM courses c
            JOIN grades g ON c.id = g.course_id
            GROUP BY c.id, c.title
            ORDER BY avg_grade DESC
        """
        df = pd.read_sql(query, engine)
        overall_mean = df['avg_grade'].mean()
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(df['course_name'], df['avg_grade'], color='#E76F51', alpha=0.8)
        ax.axhline(overall_mean, color='green', linestyle='--', linewidth=2, label=f'Overall Mean = {overall_mean:.2f}')
        ax.set_xlabel('Course')
        ax.set_ylabel('Average Grade')
        ax.set_title('Average Grade by Course')
        ax.legend()
        plt.xticks(rotation=45, ha='right')
        ax.grid(True, alpha=0.3, axis='y')
        for bar, val in zip(bars, df['avg_grade']):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,f'{val:.2f}', ha='center', va='bottom', fontsize=9)
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        print(f"Error: {e}")
        return "Error", 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
