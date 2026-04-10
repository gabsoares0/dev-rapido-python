from flask import Flask, request, jsonify

app = Flask(DESAFIO BISPO)


@app.route("/api/calculadora", methods=["POST"])
def calculadora():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum JSON foi enviado."}), 400

    a = dados.get("a")
    b = dados.get("b")
    operacao = dados.get("operacao")

    if a is None or b is None or operacao is None:
        return jsonify({
            "erro": "Os campos 'a', 'b' e 'operacao' são obrigatórios."
        }), 400

    try:
        a = float(a)
        b = float(b)
    except (ValueError, TypeError):
        return jsonify({
            "erro": "Os valores de 'a' e 'b' devem ser numéricos."
        }), 400

    operacao = operacao.lower()

    if operacao == "soma":
        resultado = a + b
    elif operacao == "subtracao":
        resultado = a - b
    elif operacao == "multiplicacao":
        resultado = a * b
    elif operacao == "divisao":
        if b == 0:
            return jsonify({"erro": "Não é possível dividir por zero."}), 400
        resultado = a / b
    else:
        return jsonify({
            "erro": "Operação inválida. Use: soma, subtracao, multiplicacao ou divisao."
        }), 400

    return jsonify({
        "a": a,
        "b": b,
        "operacao": operacao,
        "resultado": resultado
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
