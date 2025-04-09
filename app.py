from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample inventory data (replace with database later)
inventory = [
    {'id': 1, 'name': 'Laptop', 'quantity': 50, 'price': 1200},
    {'id': 2, 'name': 'Mouse', 'quantity': 200, 'price': 25},
    {'id': 3, 'name': 'Keyboard', 'quantity': 150, 'price': 75}
]

@app.route('/')
def index():
    return render_template('index.html', inventory=inventory)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        # Get item details from the form
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])

        # Create a new item (in a real app, you'd interact with a database)
        new_item = {
            'id': len(inventory) + 1,
            'name': name,
            'quantity': quantity,
            'price': price
        }
        inventory.append(new_item)
        return redirect(url_for('index'))
    else:
        return render_template('add_item.html')

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = next((item for item in inventory if item['id'] == item_id), None)
    if item is None:
        return "Item not found", 404

    if request.method == 'POST':
        # Update item details from the form
        item['name'] = request.form['name']
        item['quantity'] = int(request.form['quantity'])
        item['price'] = float(request.form['price'])
        return redirect(url_for('index'))
    else:
        return render_template('edit_item.html', item=item)

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    global inventory
    inventory = [item for item in inventory if item['id'] != item_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
