from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.models import db, Question, Category
from schemas.question import CategoryResponse, CategoryCreate


categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/', methods=['GET'])
def get_categories():
    categories = db.session.query(Category).all()

    categories_data = [
        CategoryResponse.model_validate(cat).model_dump()
        for cat in categories
    ]

    return jsonify(categories_data), 200


@categories_bp.route('/', methods=['POST'])
def create_category():
    try:
        category_data = CategoryCreate.model_validate_json(request.data)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    category_data = category_data.model_dump()

    category = Category(**category_data)
    db.session.add(category)
    db.session.commit()

    return jsonify(CategoryResponse.model_validate(category).model_dump()), 201


@categories_bp.route('/<int:id>', methods=['PUT'])
def update_category(id):
    category = db.session.query(Category).filter(Category.id == id).one_or_none()
    if not category:
        return jsonify({'message': "Категория с таким ID не найдена"}), 404

    try:
        data = CategoryCreate.model_validate_json(request.data)
    except ValidationError as err:
        return jsonify(err.errors()), 400

    data: dict = data.model_dump()

    for column, value in data.items():
        setattr(category, column, value)

    db.session.commit()
    return jsonify({'message': f"Категория обновлена: {category.name}"}), 200


@categories_bp.route('/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = db.session.query(Category).filter(Category.id == id).one_or_none()
    if category is None:
        return jsonify({'message': "Категория с таким ID не найдена"}), 404

    db.session.delete(category)
    db.session.commit()

    return jsonify({'message': f"Категория с ID {id} удалена"}), 200

