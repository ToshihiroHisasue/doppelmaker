from flask import Flask, request, render_template

app = Flask(__name__)

# 質問ごとの重み付け
weights = {
    "q1": {
        "Logical-analytical reasoning": 0.4,
        "Adaptability in learning new skills": 0.2,
        "Creativity and divergent thinking": 0.1,
        "Stress tolerance and resilience": -0.1,
        "Playfulness and humor": -0.4,
    },
    "q2": {
        "Creativity and divergent thinking": 0.4,
        "Logical-analytical reasoning": 0.2,
        "Originality in self-expression": 0.1,
        "Social adaptability": -0.1,
        "Physical stamina and endurance": -0.2,
    },
    "q3": {
        "Spatial intelligence": 0.4,
        "Logical-analytical reasoning": 0.2,
        "Kinesthetic intelligence": 0.1,
        "Artistic creativity": -0.1,
        "Empathy and perspective-taking": -0.2,
    },
    "q4": {
        "Memory and information retention": 0.4,
        "Adaptability in learning new skills": 0.2,
        "Logical-analytical reasoning": 0.1,
        "Playfulness and humor": -0.1,
        "Physical stamina and endurance": -0.2,
    },
    "q5": {
        "Adaptability in learning new skills": 0.4,
        "Memory and information retention": 0.2,
        "Stress tolerance and resilience": 0.1,
        "Kinesthetic intelligence": -0.1,
        "Artistic creativity": -0.2,
    },
    "q6": {
        "Emotional regulation": 0.4,
        "Stress tolerance and resilience": 0.2,
        "Empathy and perspective-taking": 0.1,
        "Adaptability in learning new skills": 0.1,
        "Logical-analytical reasoning": -0.2,
        "Artistic creativity": -0.4,
    },
    "q7": {
        "Stress tolerance and resilience": 0.4,
        "Emotional regulation": 0.1,
        "Sense of purpose or life meaning": 0.05,
        "Adaptability in learning new skills": 0.1,
        "Artistic creativity": -0.1,
        "Kinesthetic intelligence": -0.2,
    },
    "q8": {
        "Optimism and positivity": 0.4,
        "Sense of purpose or life meaning": 0.05,
        "Stress tolerance and resilience": 0.1,
        "Adaptability in learning new skills": 0.1,
        "Logical-analytical reasoning": -0.1,
        "Kinesthetic intelligence": -0.2,
    },
    "q9": {
        "Empathy and perspective-taking": 0.2,
        "Relationship-building": 0.2,
        "Communication skills": 0.1,
        "Emotional regulation": 0.1,
        "Logical-analytical reasoning": -0.1,
        "Artistic creativity": -0.2,
        "Stress tolerance and resilience": -0.2,
    },
    "q10": {
        "Sense of purpose or life meaning": 0.2,
        "Optimism and positivity": 0.2,
        "Emotional regulation": 0.1,
        "Curiosity and openness to new ideas": 0.1,
        "Playfulness and humor": -0.1,
        "Kinesthetic intelligence": -0.2,
    },
    "q11": {
        "Physical stamina and endurance": 0.6,
        "Strength and flexibility": 0.3,
        "Kinesthetic intelligence": 0.1,
        "Optimism and positivity": 0.1,
        "Storytelling and narrative abilities": -0.1,
        "Curiosity and openness to new ideas": -0.2,
    },
    "q12": {
        "Strength and flexibility": 0.5,
        "Kinesthetic intelligence": 0.3,
        "Physical stamina and endurance": 0.1,
        "Optimism and positivity": 0.1,
        "Logical-analytical reasoning": -0.1,
        "Empathy and perspective-taking": -0.2,
    },
    "q13": {
        "Health metrics": 0.6,
        "Physical stamina and endurance": 0.3,
        "Strength and flexibility": 0.1,
        "Optimism and positivity": 0.1,
        "Empathy and perspective-taking": -0.1,
        "Storytelling and narrative abilities": -0.2,
    },
    "q14": {
        "Sensory acuity": 0.6,
        "Kinesthetic intelligence": 0.3,
        "Physical stamina and endurance": 0.1,
        "Spatial intelligence": 0.1,
        "Empathy and perspective-taking": -0.1,
        "Optimism and positivity": -0.2,
    },
    "q15": {
        "Kinesthetic intelligence": 0.6,
        "Strength and flexibility": 0.3,
        "Physical stamina and endurance": 0.1,
        "Sensory acuity": 0.1,
        "Logical-analytical reasoning": -0.1,
        "Storytelling and narrative abilities": -0.2,
    },
    "q16": {
        "Communication skills": 0.4,
        "Relationship-building": 0.2,
        "Collaboration and teamwork": 0.1,
        "Empathy and perspective-taking": 0.05,
        "Logical-analytical reasoning": -0.1,
        "Moral reasoning and integrity": -0.2,
    },
    "q17": {
        "Collaboration and teamwork": 0.4,
        "Communication skills": 0.2,
        "Relationship-building": 0.1,
        "Empathy and perspective-taking": 0.05,
        "Playfulness and humor": -0.1,
        "Spirituality or existential inquiry": -0.2,
    },
    "q18": {
        "Leadership tendencies": 0.4,
        "Communication skills": 0.2,
        "Logical-analytical reasoning": 0.1,
        "Empathy and perspective-taking": 0.05,
        "Playfulness and humor": -0.1,
        "Spirituality or existential inquiry": -0.2,
    },
    "q19": {
        "Social adaptability": 0.4,
        "Empathy and perspective-taking": 0.2,
        "Collaboration and teamwork": 0.1,
        "Optimism and positivity": 0.1,
        "Logical-analytical reasoning": -0.1,
        "Artistic creativity": -0.2,
    },
    "q20": {
        "Relationship-building": 0.4,
        "Empathy and perspective-taking": 0.1,
        "Collaboration and teamwork": 0.1,
        "Communication skills": 0.1,
        "Curiosity and openness to new ideas": -0.1,
        "Artistic creativity": -0.2,
    },
    "q21": {
        "Moral reasoning and integrity": 0.8,
        "Empathy and perspective-taking": 0.01,
        "Sense of purpose or life meaning": 0.1,
        "Logical-analytical reasoning": 0.1,
        "Playfulness and humor": -0.1,
        "Artistic creativity": -0.2,
    },
    "q22": {
        "Altruism and generosity": 0.8,
        "Empathy and perspective-taking": 0.05,
        "Sense of purpose or life meaning": 0.1,
        "Communication skills": 0.1,
        "Artistic creativity": -0.1,
        "Sensory acuity": -0.2,
    },
    "q23": {
        "Curiosity and openness to new ideas": 0.8,
        "Creativity and divergent thinking": 0.2,
        "Empathy and perspective-taking": 0.1,
        "Sense of purpose or life meaning": 0.05,
        "Social adaptability": -0.1,
        "Kinesthetic intelligence": -0.2,
    },
    "q24": {
        "Self-awareness": 0.4,
        "Sense of purpose or life meaning": 0.05,
        "Empathy and perspective-taking": 0.1,
        "Logical-analytical reasoning": 0.1,
        "Collaboration and teamwork": -0.1,
        "Optimism and positivity": -0.2,
    },
    "q25": {
        "Spirituality or existential inquiry": 0.8,
        "Sense of purpose or life meaning": 0.2,
        "Empathy and perspective-taking": 0.1,
        "Self-awareness": 0.1,
        "Logical-analytical reasoning": -0.1,
        "Kinesthetic intelligence": -0.2,
    },
    "q26": {
        "Artistic creativity": 0.8,
        "Originality in self-expression": 0.4,
        "Appreciation of beauty": 0.1,
        "Empathy and perspective-taking": 0.1,
        "Logical-analytical reasoning": -0.1,
        "Physical stamina and endurance": -0.2,
    },
    "q27": {
        "Appreciation of beauty": 0.8,
        "Artistic creativity": 0.4,
        "Empathy and perspective-taking": 0.1,
        "Spirituality or existential inquiry": 0.1,
        "Social adaptability": -0.1,
        "Strength and flexibility": -0.2,
    },
    "q28": {
        "Originality in self-expression": 0.8,
        "Creativity and divergent thinking": 0.4,
        "Artistic creativity": 0.1,
        "Appreciation of beauty": 0.1,
        "Collaboration and teamwork": -0.1,
        "Social adaptability": -0.2,
    },
    "q29": {
        "Storytelling and narrative abilities": 0.8,
        "Communication skills": 0.4,
        "Empathy and perspective-taking": 0.1,
        "Creativity and divergent thinking": 0.1,
        "Physical stamina and endurance": -0.1,
        "Health metrics": -0.2,
    },
    "q30": {
        "Playfulness and humor": 0.8,
        "Creativity and divergent thinking": 0.4,
        "Social adaptability": 0.1,
        "Empathy and perspective-taking": 0.1,
        "Moral reasoning and integrity": -0.1,
        "Logical-analytical reasoning": -0.2,
    },
     
    # 他の質問も同様に設定
}

# 大カテゴリーとサブカテゴリーの対応付け
categories = {
    "Cognitive": [
        "Logical-analytical reasoning",
        "Creativity and divergent thinking",
        "Spatial intelligence",
        "Memory and information retention",
        "Adaptability in learning new skills"
    ],
    "Emotional": [
        "Emotional regulation",
        "Stress tolerance and resilience",
        "Optimism and positivity",
        "Empathy and perspective-taking",
        "Sense of purpose or life meaning"
    ],
    "Physical": [
        "Physical stamina and endurance",
        "Strength and flexibility",
        "Health metrics",
        "Sensory acuity",
        "Kinesthetic intelligence"
    ],
    "Social": [
        "Communication skills",
        "Collaboration and teamwork",
        "Leadership tendencies",
        "Social adaptability",
        "Relationship-building"
    ],
    "Ethical": [
        "Moral reasoning and integrity",
        "Altruism and generosity",
        "Curiosity and openness to new ideas",
        "Self-awareness",
        "Spirituality or existential inquiry"
    ],
    "Aesthetic": [
        "Artistic creativity",
        "Appreciation of beauty",
        "Originality in self-expression",
        "Storytelling and narrative abilities",
        "Playfulness and humor"
    ]
}

# 質問ページの表示
@app.route("/")
def questions():
    return render_template("questions.html")

# フォーム送信後の処理
@app.route("/submit", methods=["POST"])
def submit():
    # ユーザーの回答を取得
    responses = {key: int(value) for key, value in request.form.items()}

    # サブカテゴリーごとのスコアを初期化
    subcategory_scores = {subcategory: 9 for category in categories.values() for subcategory in category}

    # 質問ごとのスコアを反映
    for question, answer in responses.items():
        if question in weights:
            for subcategory, weight in weights[question].items():
                subcategory_scores[subcategory] += answer * weight
    # サブカテゴリーごとのスコアを四捨五入
    subcategory_scores = {
        subcategory: round(score, 1) for subcategory, score in subcategory_scores.items()
    }

    # 大カテゴリーごとのスコアを計算
    category_scores = {
        category: round(sum(subcategory_scores[subcategory] for subcategory in subcategories), 1)
        for category, subcategories in categories.items()
    }

    subcategory_translations = {
        "Logical-analytical reasoning": "論理的・分析的思考",
        "Creativity and divergent thinking": "創造性・発散的思考",
        "Spatial intelligence": "空間的把握能力",
        "Memory and information retention": "記憶力と情報保持",
        "Adaptability in learning new skills": "新しいスキルへの適応力",
        "Emotional regulation": "感情のコントロール",
        "Stress tolerance and resilience": "ストレス耐性と回復力",
        "Optimism and positivity": "楽観性と前向きな姿勢",
        "Empathy and perspective-taking": "共感と視点の共有",
        "Sense of purpose or life meaning": "目的意識または人生の意義",
        "Physical stamina and endurance": "体力と持久力",
        "Strength and flexibility": "筋力と柔軟性",
        "Health metrics": "健康指標",
        "Sensory acuity": "感覚の鋭敏さ",
        "Kinesthetic intelligence": "身体運動知能",
        "Communication skills": "コミュニケーションスキル",
        "Collaboration and teamwork": "協力とチームワーク",
        "Leadership tendencies": "リーダーシップの傾向",
        "Social adaptability": "社会適応力",
        "Relationship-building": "関係構築",
        "Moral reasoning and integrity": "道徳的思考と誠実さ",
        "Altruism and generosity": "利他主義と寛大さ",
        "Curiosity and openness to new ideas": "好奇心と新しいアイデアへの開放性",
        "Self-awareness": "自己認識",
        "Spirituality or existential inquiry": "精神性または存在の探求",
        "Artistic creativity": "芸術的創造性",
        "Appreciation of beauty": "美しさの鑑賞",
        "Originality in self-expression": "自己表現の独創性",
        "Storytelling and narrative abilities": "物語構築と叙述能力",
        "Playfulness and humor": "遊び心とユーモア"
    }


    # サブカテゴリーと大カテゴリーのスコアを結果ページに渡す
    return render_template(
        "result.html",
        category_scores=category_scores,
        subcategory_scores=subcategory_scores,
        subcategory_translations=subcategory_translations,  # 追加
        cognitive_subcategories=["Logical-analytical reasoning", "Creativity and divergent thinking", "Spatial intelligence", "Memory and information retention", "Adaptability in learning new skills"],
        emotional_subcategories=["Emotional regulation", "Stress tolerance and resilience", "Optimism and positivity", "Empathy and perspective-taking", "Sense of purpose or life meaning"],
        physical_subcategories=["Physical stamina and endurance", "Strength and flexibility", "Health metrics", "Sensory acuity", "Kinesthetic intelligence"],
        social_subcategories=["Communication skills", "Collaboration and teamwork", "Leadership tendencies", "Social adaptability", "Relationship-building"],
        ethical_subcategories=["Moral reasoning and integrity", "Altruism and generosity", "Curiosity and openness to new ideas", "Self-awareness", "Spirituality or existential inquiry"],
        aesthetic_subcategories=["Artistic creativity", "Appreciation of beauty", "Originality in self-expression", "Storytelling and narrative abilities", "Playfulness and humor"]
    )




if __name__ == "__main__":
    app.run(debug=True)