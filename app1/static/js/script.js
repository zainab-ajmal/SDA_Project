const addBtn = document.getElementById("add")

const notes = JSON.parse(localStorage.getItem("notes"))

if (notes) {
  notes.forEach(function (note) {
    addNewNote(note)
  })
}

addBtn.addEventListener("click", function () {
  addNewNote()
})

function addNewNote(text = "") {
  const note = document.createElement("div")
  note.classList.add("note")

  note.innerHTML = `
    <div class="tools">
        <button class="edit">
            <i class="fas fa-edit"></i>
        </button>
        <button class="delete">
            <fas class="fas fa-trash-alt"></fas>
        </button>
    </div>

    <div class="main ${text ? "" : "hidden"}"></div>
    <textarea class="${text ? "hidden" : ""}"></textarea>
  `

  const editBtn = note.querySelector(".edit")
  const deleteBtn = note.querySelector(".delete")
  const main = note.querySelector(".main")
  const textArea = note.querySelector("textarea")
  main.innerHTML = marked(text)

  deleteBtn.addEventListener("click", function () {
    note.remove()

    updateLS()
  })

  editBtn.addEventListener("click", function () {
    main.classList.toggle("hidden")
    textArea.classList.toggle("hidden")
  })

  textArea.addEventListener("input", function (e) {
    const { value } = e.target

    main.innerHTML = marked(value)

    updateLS()
  })

  document.body.appendChild(note)
}

function updateLS() {
  const noteText = document.querySelectorAll("textarea")

  const notes = []

  noteText.forEach(function (note) {
    notes.push(note.value)
  })

  localStorage.setItem("notes", JSON.stringify(notes))
}