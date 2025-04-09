import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from supabase import create_client, Client

app = Flask(__name__)
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    response = supabase.table('inventory').select("*").execute()
    inventory = response.data
    return render_template('index.html', inventory=inventory)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])

        # Insert the new item into the database
        data = {"name": name, "quantity": quantity, "price": price}
        response = supabase.table('inventory').insert(data).execute()

        return redirect(url_for('index'))
    else:
        return render_template('add_item.html')

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    response = supabase.table('inventory').select("*").eq('id', item_id).execute()
    item = response.data[0] if response.data else None

    if item is None:
        return "Item not found", 404

    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])

        # Update the item in the database
        data = {"name": name, "quantity": quantity, "price": price}
        response = supabase.table('inventory').update(data).eq('id', item_id).execute()
        return redirect(url_for('index'))
    else:
        return render_template('edit_item.html', item=item)

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    response = supabase.table('inventory').delete().eq('id', item_id).execute()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
