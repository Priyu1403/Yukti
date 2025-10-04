# Enterprise Expense Management — Odoo Module

## Quick install
1. Copy the `enterprise_expense_mgmt` folder into your Odoo `addons` directory.
2. Restart Odoo server.
3. Update Apps list in Odoo (Apps -> Update Apps List) and search for "Enterprise Expense Management".
4. Install the module.
5. Go to `Expenses -> Expense Management -> All Expenses` to start.

## Roles
- Create users and add them to the groups: Expense: Employee, Expense: Manager, Expense: Finance (Settings -> Users -> Groups).

## Demo
- The demo record shows one submitted expense. Use it to test approval flow.

## Extend
- Connect to `account.move` when finance approves to create journal entries.
- Add OCR for receipts if you want to extract amount and vendor.
- Add budgets per department and alerts.
