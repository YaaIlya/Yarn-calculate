// app.js

let yarns = [];

// Функция для обновления списка пряжи
function updateYarnList() {
    const yarnList = document.querySelector('.yarn-list');
    yarnList.innerHTML = '';

    yarns.forEach((yarn, index) => {
        const listItem = document.createElement('li');
        listItem.classList.add('yarn-item');
        listItem.innerHTML = `
            <span>${index + 1}. ${yarn.brand} - ${yarn.name} (${yarn.color}, ${yarn.quantity}шт.)</span>
            <button class="button delete-button" data-index="${index}">Удалить</button>
        `;
        yarnList.appendChild(listItem);
    });

    // Добавляем обработчики удаления
    document.querySelectorAll('.delete-button').forEach(button => {
        button.addEventListener('click', function() {
            const index = this.dataset.index;
            yarns.splice(index, 1);
            updateYarnList();
        });
    });
}

// Добавление новой пряжи
document.getElementById("add-yarn-button").addEventListener("click", function() {
    const brand = prompt("Введите фирму пряжи:");
    const name = prompt("Введите название пряжи:");
    const country = prompt("Введите страну производства:");
    const color = prompt("Введите цвет пряжи:");
    const quantity = parseInt(prompt("Введите количество пряжи:"));

    if (brand && name && country && color && !isNaN(quantity)) {
        yarns.push({ brand, name, country, color, quantity });
        updateYarnList();
    } else {
        alert("Пожалуйста, заполните все поля корректно.");
    }
});

// Удаление всей пряжи
document.getElementById("delete-all-button").addEventListener("click", function() {
    if (confirm("Вы уверены, что хотите удалить всю пряжу?")) {
        yarns = [];
        updateYarnList();
    }
});
