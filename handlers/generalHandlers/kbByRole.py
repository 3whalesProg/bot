import db
from handlers.foremanHandler import foreman_kb
from handlers.supplierHandler import supplier_kb
from handlers.adminHandler import admin_kb

async def takeRoleKb(userId):
    role = db.checkRole(userId)
    if role == 'Снабженец':
        return supplier_kb.supplier
    if role == 'Прораб':
        return foreman_kb.foreman
    if role == 'Админ':
        return admin_kb.base