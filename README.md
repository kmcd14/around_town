# Agile methodology for Around Town 

##  Product Backlog

| ID  | User Story                                                            | Priority | Status | Sprint   |
| --- | --------------------------------------------------------------------- | -------- | ------ | -------- |
| US1 | As a user, I want to easily and quickly find local groups in the area | High     | Done   | Sprint 1 |
| US1 | As a user, I want to filter groups by category                        | High     | Done   | Sprint 1 |
| US2 | As a user, I want to filter groups by age group                       | High     | Done   | Sprint 1 |
| US3 | As a user, I want to filter groups by area                            | High     | Done   | Sprint 1 |
| US4 | As a user, I want a search bar to find groups quickly                 | High     | Done   | Sprint 2 |
| US5 | As a user, I want a visually appealing sidebar                        | Medium   | Done   | Sprint 2 |
| US6 | As a user, I want the main content styled and readable                | Medium   | Done   | Sprint 2 |
| US7 | As a user, I want to view visual insights of groups                   | Low      | Done   | Sprint 3 |
| US8 | As a user, I want better colors for input fields and group names      | Medium   | Done   | Sprint 3 |


---

## 📝 Sprint Log

### Sprint 1 (April 19 – May 12)

* Signed up for Supabase and created database
* Created SQLAlchemy models for `Group` and `Category`
* Connected to the database with a session manager
* Imported researched local group data into Supabase using Google Sheets/CSV
* Created Google Form for user-submitted groups
* Added sidebar filters: category, age group, area and Google form submission link

### Sprint 2 (May 13 – May 15)

* Implemented search bar in main area
* Styled sidebar using CSS (colors, font, layout)
* Styled main content section and input fields
* Began mobile responsiveness testing

### Sprint 3 (May 16 – May 18)

* Customized colors of search bar and group name headers
* Created insights tab with Plotly charts
* Improved layout spacing and card readability
* Began exploring sidebar visibility on mobile

---

## 🤔 Retrospective – Sprint 3

### ✅ What went well:

* Search functionality is clear and effective
* Visual styling improved UX significantly
* CSS extraction helped keep code clean

### 🙁 What could be improved:

* Sidebar not easily accessible on mobile
* CSS occasionally caused style conflicts

### 🔁 Action Items:

* Explore automatic sidebar visibility using custom JavaScript

---

## 🧰 Agile Tools Used

* **Streamlit** for rapid UI iteration
* **Markdown** files for backlog and sprint logs
* **Supabase** for real-time database setup and hosting
* **Google Sheets/CSV** for batch uploading group data
* **Google Forms** for user-submitted group input
* **Version control** via Git for commits per sprint

