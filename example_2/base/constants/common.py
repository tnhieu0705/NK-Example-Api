class AppConstants:
    class Role:
        Admin = 1
        User = 2
        Customer = 3
        Vendor = 4

    class RoleOrder:
        Cart = 1
        Pending = 2


class AppChoices:
    RolesForRegister = [
        (AppConstants.Role.Admin, 'Admin'),
        (AppConstants.Role.User, 'User')
    ]

    RolesForAdminManageUsers = [
        (AppConstants.Role.Admin, 'Admin'),
        (AppConstants.Role.User, 'User'),
        (AppConstants.Role.Customer, 'Customer'),
        (AppConstants.Role.Vendor, 'Vendor')
    ]

    RolesForOrder = [
        (AppConstants.RoleOrder.Cart, 'in_cart'),
        (AppConstants.RoleOrder.Pending, 'pending')
    ]


class ValidationMessages:
    PasswordsDoesNotMatch = 'Passwords does not match.'
