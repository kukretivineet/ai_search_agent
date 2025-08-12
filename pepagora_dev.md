# MongoDB Schema: `pepagora_dev`

**Generated on:** 2025-08-11 13:30:07
**Database:** `pepagora_dev`
**Total Collections:** 36

## Table of Contents

- [admin_users](#admin-users)
- [admingroups](#admingroups)
- [admins](#admins)
- [adminusers](#adminusers)
- [application](#application)
- [billingdetails](#billingdetails)
- [businessprofiles](#businessprofiles)
- [buyingrequests](#buyingrequests)
- [catalog_datas](#catalog-datas)
- [catalogs](#catalogs)
- [categories](#categories)
- [client_sessions](#client-sessions)
- [contents](#contents)
- [customers](#customers)
- [enquiries](#enquiries)
- [exchangerates](#exchangerates)
- [filters](#filters)
- [leads](#leads)
- [liveproducts](#liveproducts)
- [marketcatalogs](#marketcatalogs)
- [messages](#messages)
- [otps](#otps)
- [payments](#payments)
- [productcategories](#productcategories)
- [quotations](#quotations)
- [remarks](#remarks)
- [reviews](#reviews)
- [rfqcarts](#rfqcarts)
- [roles](#roles)
- [salesproductgroups](#salesproductgroups)
- [salesproductionleadtimes](#salesproductionleadtimes)
- [salesproducts](#salesproducts)
- [selloffers](#selloffers)
- [sessions](#sessions)
- [subcategories](#subcategories)
- [users](#users)

## admin_users

**Document Count:** 0
**Sample Size:** 0

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## admingroups

**Document Count:** 4
**Sample Size:** 4

### Fields

| Field                                              | Type          | Example                                   |
| -------------------------------------------------- | ------------- | ----------------------------------------- |
| `__v`                                              | integer       | 0                                         |
| `_id`                                              | ObjectId      |                                           |
| `allowedModules`                                   | array<object> |                                           |
| `allowedModules[].moduleDescription`               | string        | View dashboard                            |
| `allowedModules[].moduleName`                      | string        | Dashboard                                 |
| `allowedModules[].permissions`                     | object        |                                           |
| `allowedModules[].permissions.create`              | boolean       | False                                     |
| `allowedModules[].permissions.delete`              | boolean       | False                                     |
| `allowedModules[].permissions.edit`                | boolean       | False                                     |
| `allowedModules[].submodules`                      | array<object> |                                           |
| `allowedModules[].submodules[].moduleDescription`  | string        | View onboarding approvals                 |
| `allowedModules[].submodules[].moduleName`         | string        | Onboarding Approvals                      |
| `allowedModules[].submodules[].permissions`        | object        |                                           |
| `allowedModules[].submodules[].permissions.create` | boolean       | False                                     |
| `allowedModules[].submodules[].permissions.delete` | boolean       | False                                     |
| `allowedModules[].submodules[].permissions.edit`   | boolean       | False                                     |
| `createdAt`                                        | date          |                                           |
| `groupDescription`                                 | string        | Read-only access to dashboard and reports |
| `groupName`                                        | string        | View Only                                 |
| `isActive`                                         | boolean       | True                                      |
| `isDeleted`                                        | boolean       | False                                     |
| `metadata`                                         | object        |                                           |
| `metadata.level`                                   | string        | low                                       |
| `tags`                                             | array<string> |                                           |
| `updatedAt`                                        | date          |                                           |
| `users`                                            | array (empty) |                                           |

### First Document (sanitized)

```json
{
  "_id": "6874d1ddd11244886dd2e757",
  "groupName": "Super Admin",
  "groupDescription": "Full system access with all permissions",
  "allowedModules": [
    {
      "moduleName": "Dashboard",
      "moduleDescription": "Complete dashboard access",
      "permissions": {
        "delete": true,
        "create": true,
        "edit": true
      },
      "submodules": [
        {
          "moduleName": "Onboarding Approvals",
          "moduleDescription": "Manage onboarding approvals",
          "permissions": {
            "delete": true,
            "create": true,
            "edit": true
          }
        },
        {
          "moduleName": "Product Approvals",
          "moduleDescription": "Manage product approvals",
          "permissions": {
            "delete": true,
            "create": true,
            "edit": true
          }
        },
        {
          "moduleName": "Client & Membership",
          "moduleDescription": "Manage client memberships",
          "permissions": {
            "delete": true,
            "create": true,
            "edit": true
          }
        },
        {
          "moduleName": "Catalog Approval",
          "moduleDescription": "Manage catalog approvals",
          "permissions": {
            "delete": true,
            "create": true,
            "edit": true
          }
        },
        {
          "moduleName": "Sell offer Approval",
          "moduleDescription": "Manage sell offer approvals",
          "permissions": {
            "delete": true,
            "create": true,
            "edit": true
          }
        },
        "[... truncated ...]"
      ]
    },
    {
      "moduleName": "User Management",
      "moduleDescription": "Complete user management access",
      "permissions": {
        "delete": true,
        "create": true,
        "edit": true
      },
      "submodules": [
        {
          "moduleName": "Users",
          "moduleDescription": "Manage users",
          "permissions": {
            "delete": true,
            "create": true,
            "edit": true
          }
        },
        {
          "moduleName": "Access Setup",
          "moduleDescription": "Manage access setup",
          "permissions": {
            "delete": true,
            "create": true,
            "edit": true
          }
        }
      ]
    },
    {
      "moduleName": "Portal Management",
      "moduleDescription": "Complete portal management access",
      "permissions": {
        "delete": true,
        "create": true,
        "edit": true
      },
      "submodules": [
        {
          "moduleName": "CMS",
          "moduleDescription": "Manage CMS",
          "permissions": {
            "delete": true,
            "create": true,
            "edit": true
          }
        },
        {
          "moduleName": "Tag Management",
          "moduleDescription": "Manage tags",
          "permissions": {
            "delete": true,
            "create": true,
            "edit": true
          }
        },
        {
          "moduleName": "Category Management",
          "moduleDescription": "Manage categories",
          "permissions": {
            "delete": true,
            "create": true,
            "edit": true
          }
        }
      ]
    },
    {
      "moduleName": "Report & Analysis",
      "moduleDescription": "Complete report and analysis access",
      "permissions": {
        "delete": true,
        "create": true,
        "edit": true
      },
      "submodules": [
        {
          "moduleName": "Product Based",
          "moduleDescription": "Product based reports",
          "permissions": {
            "delete": true,
            "create": true,
            "edit": true
          }
        },
        {
          "moduleName": "Account/User Based",
          "moduleDescription": "Account/User based reports",
          "permissions": {
            "delete": true,
            "create": true,
            "edit": true
          }
        },
        {
          "moduleName": "Catalog Based",
          "moduleDescription": "Catalog based reports",
          "permissions": {
            "delete": true,
            "create": true,
            "edit": true
          }
        },
        {
          "moduleName": "Enquiry Based",
          "moduleDescription": "Enquiry based reports",
          "permissions": {
            "delete": true,
            "create": true,
            "edit": true
          }
        }
      ]
    },
    {
      "moduleName": "Support",
      "moduleDescription": "Complete support access",
      "permissions": {
        "delete": true,
        "create": true,
        "edit": true
      },
      "submodules": [
        {
          "moduleName": "Feedback Management",
          "moduleDescription": "Manage feedback",
          "permissions": {
            "delete": true,
            "create": true,
            "edit": true
          }
        }
      ]
    }
  ],
  "isActive": true,
  "isDeleted": false,
  "tags": ["super-admin", "full-access"],
  "users": [],
  "metadata": {
    "level": "highest"
  },
  "createdAt": "2025-07-14T09:46:05.229000",
  "updatedAt": "2025-07-14T09:46:05.229000",
  "__v": 0
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

**groupName_1**

- Type: Unique
- Keys:
  - `groupName`: ascending

**name_1**

- Keys:
  - `name`: ascending

**isActive_1**

- Keys:
  - `isActive`: ascending

**isDeleted_1**

- Keys:
  - `isDeleted`: ascending

**createdAt\_-1**

- Keys:
  - `createdAt`: descending

---

## admins

**Document Count:** 5
**Sample Size:** 5

### Fields

| Field                                   | Type          | Example                         |
| --------------------------------------- | ------------- | ------------------------------- |
| `__v`                                   | integer       | 0                               |
| `_id`                                   | ObjectId      |                                 |
| `activeSessions`                        | array (empty) |                                 |
| `activityLog`                           | array<object> |                                 |
| `activityLog[].action`                  | string        | ACCOUNT_CREATED                 |
| `activityLog[].description`             | string        | Account created via seed script |
| `activityLog[].ipAddress`               | string        | 127.0.0.1                       |
| `activityLog[].status`                  | string        | success                         |
| `activityLog[].targetEntity`            | string        | Admin                           |
| `activityLog[].targetId`                | string        | seed-script                     |
| `activityLog[].timestamp`               | date          |                                 |
| `activityLog[].userAgent`               | string        | Seed Script                     |
| `assignments`                           | array (empty) |                                 |
| `createdAt`                             | date          |                                 |
| `email`                                 | string        | support.admin@pepagora.com      |
| `isActive`                              | boolean       | True                            |
| `isBlocked`                             | boolean       | False                           |
| `isDeleted`                             | boolean       | False                           |
| `isEmailVerified`                       | boolean       | True                            |
| `isPhoneVerified`                       | boolean       | True                            |
| `isSuperAdmin`                          | boolean       | False                           |
| `isSuspended`                           | boolean       | False                           |
| `lastLoginAt`                           | date          |                                 |
| `lastPasswordChange`                    | date          |                                 |
| `metadata`                              | object        |                                 |
| `metadata.department`                   | string        | Customer Support                |
| `metadata.level`                        | string        | admin                           |
| `notificationPreferences`               | object        |                                 |
| `notificationPreferences.email`         | boolean       | True                            |
| `notificationPreferences.inApp`         | boolean       | True                            |
| `notificationPreferences.push`          | boolean       | True                            |
| `notificationPreferences.sms`           | boolean       | True                            |
| `password`                              | string        |                                 |
| `preferredLanguage`                     | string        | en                              |
| `profile`                               | object        |                                 |
| `profile.address`                       | object        |                                 |
| `profile.address.city`                  | string        | Support City                    |
| `profile.address.country`               | string        | USA                             |
| `profile.address.state`                 | string        | Support State                   |
| `profile.address.street`                | string        | 654 Support Drive               |
| `profile.address.zipCode`               | string        | 56789                           |
| `profile.department`                    | string        | Customer Support                |
| `profile.emergencyContact`              | object        |                                 |
| `profile.emergencyContact.name`         | string        | Anna Support                    |
| `profile.emergencyContact.phone`        | string        | +1234567899                     |
| `profile.emergencyContact.relationship` | string        | Spouse                          |
| `profile.employeeId`                    | string        | EMP005                          |
| `profile.firstName`                     | string        | Michael                         |
| `profile.lastName`                      | string        | Support                         |
| `profile.phoneNumber`                   | string        | +1234567898                     |
| `profile.position`                      | string        | Support Administrator           |
| `tags`                                  | array<string> |                                 |
| `timezone`                              | string        | America/Phoenix                 |
| `twoFactorEnabled`                      | boolean       | False                           |
| `updatedAt`                             | date          |                                 |
| `userGroup`                             | ObjectId      |                                 |
| `username`                              | string        | supportadmin                    |

### First Document (sanitized)

```json
{
  "_id": "6874ad18746cd89151a73d6c",
  "email": "superadmin@pepagora.com",
  "password": "[REDACTED]",
  "username": "superadmin",
  "profile": {
    "firstName": "John",
    "lastName": "Admin",
    "phoneNumber": "+1234567890",
    "department": "IT",
    "position": "System Administrator",
    "employeeId": "EMP001",
    "emergencyContact": {
      "name": "Jane Admin",
      "relationship": "Spouse",
      "phone": "+1234567891"
    },
    "address": {
      "street": "123 Admin Street",
      "city": "Admin City",
      "state": "Admin State",
      "zipCode": "12345",
      "country": "USA"
    }
  },
  "isSuperAdmin": true,
  "userGroup": "6874ad18746cd89151a73d5f",
  "assignments": [],
  "isEmailVerified": true,
  "isPhoneVerified": true,
  "isActive": true,
  "isDeleted": false,
  "isBlocked": false,
  "isSuspended": false,
  "lastLoginAt": "2025-07-14T07:09:12.634000",
  "lastPasswordChange": "[REDACTED]",
  "activeSessions": [],
  "activityLog": [
    {
      "action": "ACCOUNT_CREATED",
      "description": "Account created via seed script",
      "targetEntity": "Admin",
      "targetId": "seed-script",
      "ipAddress": "127.0.0.1",
      "userAgent": "Seed Script",
      "timestamp": "2025-07-14T07:09:12.634000",
      "status": "success"
    }
  ],
  "twoFactorEnabled": false,
  "preferredLanguage": "en",
  "timezone": "America/New_York",
  "notificationPreferences": {
    "email": true,
    "sms": true,
    "push": true,
    "inApp": true
  },
  "tags": ["super-admin", "system"],
  "metadata": {
    "department": "IT",
    "level": "executive"
  },
  "createdAt": "2025-07-14T07:09:12.636000",
  "updatedAt": "2025-07-14T07:09:12.636000",
  "__v": 0
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

**email_1**

- Type: Unique
- Keys:
  - `email`: ascending

**username_1**

- Keys:
  - `username`: ascending

**role_1**

- Keys:
  - `role`: ascending

**isActive_1**

- Keys:
  - `isActive`: ascending

**isDeleted_1**

- Keys:
  - `isDeleted`: ascending

**createdAt\_-1**

- Keys:
  - `createdAt`: descending

**lastLoginAt\_-1**

- Keys:
  - `lastLoginAt`: descending

---

## adminusers

**Document Count:** 5
**Sample Size:** 5

### Fields

| Field                                   | Type          | Example                         |
| --------------------------------------- | ------------- | ------------------------------- |
| `__v`                                   | integer       | 0                               |
| `_id`                                   | ObjectId      |                                 |
| `activeSessions`                        | array (empty) |                                 |
| `activityLog`                           | array<object> |                                 |
| `activityLog[].action`                  | string        | ACCOUNT_CREATED                 |
| `activityLog[].description`             | string        | Account created via seed script |
| `activityLog[].ipAddress`               | string        | 127.0.0.1                       |
| `activityLog[].status`                  | string        | success                         |
| `activityLog[].targetEntity`            | string        | Admin                           |
| `activityLog[].targetId`                | string        | seed-script                     |
| `activityLog[].timestamp`               | date          |                                 |
| `activityLog[].userAgent`               | string        | Seed Script                     |
| `assignments`                           | array<object> |                                 |
| `assignments[].items`                   | array<object> |                                 |
| `assignments[].items[].assignedAt`      | date          |                                 |
| `assignments[].items[].assignedBy`      | ObjectId      |                                 |
| `assignments[].items[].id`              | ObjectId      |                                 |
| `assignments[].items[].status`          | string        | pending                         |
| `assignments[].subModuleName`           | string        | Onboarding Approvals            |
| `createdAt`                             | date          |                                 |
| `email`                                 | string        | content.manager@pepagora.com    |
| `isActive`                              | boolean       | True                            |
| `isBlocked`                             | boolean       | False                           |
| `isDeleted`                             | boolean       | False                           |
| `isEmailVerified`                       | boolean       | True                            |
| `isPhoneVerified`                       | boolean       | True                            |
| `isSuperAdmin`                          | boolean       | False                           |
| `isSuspended`                           | boolean       | False                           |
| `lastLoginAt`                           | date          |                                 |
| `lastPasswordChange`                    | date          |                                 |
| `metadata`                              | object        |                                 |
| `metadata.department`                   | string        | Marketing                       |
| `metadata.level`                        | string        | manager                         |
| `notificationPreferences`               | object        |                                 |
| `notificationPreferences.email`         | boolean       | True                            |
| `notificationPreferences.inApp`         | boolean       | True                            |
| `notificationPreferences.push`          | boolean       | True                            |
| `notificationPreferences.sms`           | boolean       | False                           |
| `password`                              | string        |                                 |
| `preferredLanguage`                     | string        | en                              |
| `profile`                               | object        |                                 |
| `profile.address`                       | object        |                                 |
| `profile.address.city`                  | string        | Content City                    |
| `profile.address.country`               | string        | USA                             |
| `profile.address.state`                 | string        | Content State                   |
| `profile.address.street`                | string        | 456 Content Avenue              |
| `profile.address.zipCode`               | string        | 23456                           |
| `profile.department`                    | string        | Marketing                       |
| `profile.emergencyContact`              | object        |                                 |
| `profile.emergencyContact.name`         | string        | Mike Content                    |
| `profile.emergencyContact.phone`        | string        | +1234567893                     |
| `profile.emergencyContact.relationship` | string        | Spouse                          |
| `profile.employeeId`                    | string        | EMP002                          |
| `profile.firstName`                     | string        | Sarah                           |
| `profile.lastName`                      | string        | Content                         |
| `profile.phoneNumber`                   | string        | +1234567892                     |
| `profile.position`                      | string        | Content Manager                 |
| `tags`                                  | array<string> |                                 |
| `timezone`                              | string        | America/Chicago                 |
| `twoFactorEnabled`                      | boolean       | False                           |
| `updatedAt`                             | date          |                                 |
| `userGroup`                             | ObjectId      |                                 |
| `username`                              | string        | contentmanager                  |

### First Document (sanitized)

```json
{
  "_id": "6874d1ddd11244886dd2e764",
  "email": "superadmin@pepagora.com",
  "password": "[REDACTED]",
  "username": "superadmin",
  "profile": {
    "firstName": "John",
    "lastName": "Admin",
    "phoneNumber": "+1234567890",
    "department": "IT",
    "position": "System Administrator",
    "employeeId": "EMP001",
    "emergencyContact": {
      "name": "Jane Admin",
      "relationship": "Spouse",
      "phone": "+1234567891"
    },
    "address": {
      "street": "123 Admin Street",
      "city": "Admin City",
      "state": "Admin State",
      "zipCode": "12345",
      "country": "USA"
    }
  },
  "isSuperAdmin": true,
  "userGroup": "6874d1ddd11244886dd2e757",
  "assignments": [
    {
      "subModuleName": "Sell offer Approval",
      "items": [
        {
          "id": "6874ba9593185d4398cf42bf",
          "assignedBy": "6874d1ddd11244886dd2e767",
          "assignedAt": "2025-07-15T10:14:13.747000",
          "status": "pending"
        },
        {
          "id": "686d378cc1973449c61d83b0",
          "assignedBy": "6874d1ddd11244886dd2e767",
          "assignedAt": "2025-07-15T10:18:59.325000",
          "status": "pending"
        },
        {
          "id": "683e8170a7ca42162866cf33",
          "assignedBy": "6874d1ddd11244886dd2e767",
          "assignedAt": "2025-07-15T11:28:47.302000",
          "status": "pending"
        },
        {
          "id": "682c27d096a14648ce7a7c24",
          "assignedBy": "6874d1ddd11244886dd2e767",
          "assignedAt": "2025-07-15T11:30:32.347000",
          "status": "pending"
        },
        {
          "id": "6874ba9593185d4398cf42bf",
          "assignedBy": "6874d1ddd11244886dd2e767",
          "assignedAt": "2025-07-15T13:15:34.255000",
          "status": "pending"
        },
        "[... truncated ...]"
      ]
    },
    {
      "subModuleName": "Sell offer Approval",
      "items": [
        {
          "id": "686d378cc1973449c61d83b0",
          "assignedBy": "6874d1ddd11244886dd2e767",
          "assignedAt": "2025-07-15T10:14:13.747000",
          "status": "pending"
        }
      ]
    },
    {
      "subModuleName": "Onboarding Approvals",
      "items": [
        {
          "id": "685b85aa523555fdc050e413",
          "assignedBy": "6874d1ddd11244886dd2e767",
          "assignedAt": "2025-07-15T13:54:28.129000",
          "status": "pending"
        },
        {
          "id": "685b89a6a8f68cc8e3c20069",
          "assignedBy": "6874d1ddd11244886dd2e767",
          "assignedAt": "2025-07-15T14:03:37.671000",
          "status": "pending"
        },
        {
          "id": "685e3e9a909298eae0b63672",
          "assignedBy": "6874d1ddd11244886dd2e767",
          "assignedAt": "2025-07-16T06:07:31.551000",
          "status": "pending"
        },
        {
          "id": "6878d1027c59fc551c9e636f",
          "assignedBy": "6874d1ddd11244886dd2e767",
          "assignedAt": "2025-07-18T13:29:44.806000",
          "status": "pending"
        },
        {
          "id": "688274c53f7178ee0dc6b0e1",
          "assignedBy": "6874d1ddd11244886dd2e767",
          "assignedAt": "2025-07-25T09:29:31.096000",
          "status": "pending"
        },
        "[... truncated ...]"
      ]
    },
    {
      "subModuleName": "RFQ Approval",
      "items": [
        {
          "id": "6874d327c24640b8b938fdd6",
          "assignedBy": "6874d1ddd11244886dd2e767",
          "assignedAt": "2025-07-15T14:05:57.320000",
          "status": "Approval Pending"
        },
        {
          "id": "686d2fe2c1973449c61d83ff",
          "assignedBy": "6874d1ddd11244886dd2e767",
          "assignedAt": "2025-07-16T05:03:59.934000",
          "status": "Approval Pending"
        },
        {
          "id": "686bf0470c647679c87df7e8",
          "assignedBy": "6874d1ddd11244886dd2e767",
          "assignedAt": "2025-07-16T05:04:30.037000",
          "status": "Approval Pending"
        },
        {
          "id": "686d2f41c1973449c61d83e8",
          "assignedBy": "6874d1ddd11244886dd2e767",
          "assignedAt": "2025-07-16T05:04:30.037000",
          "status": "Approval Pending"
        },
        {
          "id": "68709af4ae5816a7d0ba767d",
          "assignedBy": "6874d1ddd11244886dd2e767",
          "assignedAt": "2025-07-16T08:02:05.094000",
          "status": "Approval Pending"
        },
        "[... truncated ...]"
      ]
    },
    {
      "subModuleName": "Product Approvals",
      "items": [
        {
          "id": "682b210035a4cc234e16a0da",
          "assignedBy": "6874d1ddd11244886dd2e767",
          "assignedAt": "2025-07-15T14:07:36.814000",
          "status": "pending"
        },
        {
          "id": "6870bfd596c7dd13bd6010a3",
          "assignedBy": "6874d1ddd11244886dd2e767",
          "assignedAt": "2025-07-15T14:13:22.938000",
          "status": "pending"
        },
        {
          "id": "6870bfd596c7dd13bd6010a3",
          "assignedBy": "6874d1ddd11244886dd2e767",
          "assignedAt": "2025-07-15T14:15:34.359000",
          "status": "pending"
        },
        {
          "id": "68272f2f673e753d8ceab6cc",
          "assignedBy": "6874d1ddd11244886dd2e767",
          "assignedAt": "2025-07-16T04:39:19.011000",
          "status": "pending"
        },
        {
          "id": "6826ce429ad870fb6764cef9",
          "assignedBy": "6874d1ddd11244886dd2e767",
          "assignedAt": "2025-07-16T05:43:09.414000",
          "status": "pending"
        },
        "[... truncated ...]"
      ]
    }
  ],
  "isEmailVerified": true,
  "isPhoneVerified": true,
  "isActive": true,
  "isDeleted": false,
  "isBlocked": false,
  "isSuspended": false,
  "lastLoginAt": "2025-07-14T09:46:05.583000",
  "lastPasswordChange": "[REDACTED]",
  "activeSessions": [],
  "activityLog": [
    {
      "action": "ACCOUNT_CREATED",
      "description": "Account created via seed script",
      "targetEntity": "Admin",
      "targetId": "seed-script",
      "ipAddress": "127.0.0.1",
      "userAgent": "Seed Script",
      "timestamp": "2025-07-14T09:46:05.583000",
      "status": "success"
    }
  ],
  "twoFactorEnabled": false,
  "preferredLanguage": "en",
  "timezone": "America/New_York",
  "notificationPreferences": {
    "email": true,
    "sms": true,
    "push": true,
    "inApp": true
  },
  "tags": ["super-admin", "system"],
  "metadata": {
    "department": "IT",
    "level": "executive"
  },
  "createdAt": "2025-07-14T09:46:05.585000",
  "updatedAt": "2025-08-06T12:12:22.094000",
  "__v": 0
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

**email_1**

- Type: Unique
- Keys:
  - `email`: ascending

**username_1**

- Keys:
  - `username`: ascending

**role_1**

- Keys:
  - `role`: ascending

**isActive_1**

- Keys:
  - `isActive`: ascending

**isDeleted_1**

- Keys:
  - `isDeleted`: ascending

**createdAt\_-1**

- Keys:
  - `createdAt`: descending

**lastLoginAt\_-1**

- Keys:
  - `lastLoginAt`: descending

---

## application

**Document Count:** 0
**Sample Size:** 0

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## billingdetails

**Document Count:** 2
**Sample Size:** 2

### Fields

| Field                          | Type            | Example             |
| ------------------------------ | --------------- | ------------------- | --- |
| `__v`                          | integer         | 0                   |
| `_id`                          | ObjectId        |                     |
| `billingAddress`               | object          |                     |
| `billingAddress.addressLine`   | string          | 1 street            |
| `billingAddress.city`          | string          | Ghormach            |
| `billingAddress.country`       | object          |                     |
| `billingAddress.country.code`  | string          | AF                  |
| `billingAddress.country.name`  | string          | Afghanistan         |
| `billingAddress.pincode`       | string          | 123468              |
| `billingAddress.state`         | string          | Badghis             |
| `businessName`                 | string          | My Business Pvt Ltd |
| `cardExpiredDate`              | date            |                     |
| `cardHolderName`               | string          | John Doe            |
| `cardNo`                       | string          | 4111111111111111    |
| `createdAt`                    | date            |                     |
| `createdBy`                    | ObjectId        |                     |
| `cvv`                          | string          | 123                 |
| `isCompliantWithRBIGuidelines` | boolean         | False               |
| `name`                         | string          | David               |
| `payments`                     | array<ObjectId> | array (empty)       |     |
| `updatedAt`                    | date            |                     |

### First Document (sanitized)

```json
{
  "_id": "6895e6fad9316f3a545c63c0",
  "createdBy": "685b83c9640c0efe0929cfa6",
  "__v": 0,
  "billingAddress": {
    "addressLine": "1 street",
    "city": "Amguri",
    "state": "Assam",
    "pincode": "123163",
    "country": {
      "name": "India",
      "code": "IN"
    }
  },
  "businessName": "My Business Pvt Ltd",
  "createdAt": "2025-08-08T12:00:58.234000",
  "isCompliantWithRBIGuidelines": true,
  "name": "connector01",
  "payments": ["6895f7a16e675d454fa8761b"],
  "updatedAt": "2025-08-09T14:19:31.958000",
  "cardExpiredDate": "[REDACTED]",
  "cardHolderName": "[REDACTED]",
  "cardNo": "[REDACTED]",
  "cvv": "[REDACTED]"
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## businessprofiles

**Document Count:** 142
**Sample Size:** 100

### Fields

| Field                                                 | Type          | Example                                        |
| ----------------------------------------------------- | ------------- | ---------------------------------------------- | ------------------------ | ------------ |
| `BusinessVerifyStatus`                                | string        | Pending                                        |
| `IdentityVerifyStatus`                                | string        | Pending                                        |
| `PANNo`                                               | string        | asefsefewf                                     |
| `VATNo`                                               | string        |                                                |
| `__v`                                                 | integer       | 0                                              |
| `_id`                                                 | ObjectId      |                                                |
| `acceptedCurrency`                                    | array<object> |                                                |
| `acceptedCurrency[].code`                             | string        | INR                                            |
| `acceptedCurrency[].name`                             | string        | Indian Rupee                                   |
| `acceptedCurrency[].symbol`                           | string        | ₹                                              |
| `annualOutputValue`                                   | string        | Less than $1M                                  |
| `annualProductionCapacity`                            | array<object> | array (empty)                                  |                          |
| `annualProductionCapacity[].product`                  | string        | Widgets                                        |
| `annualProductionCapacity[].quantity`                 | integer       | 10000                                          |
| `annualProductionCapacity[].unit`                     | string        | pieces                                         |
| `annualTurnover`                                      | string        | Below ₹25 Lakhs                                |
| `averageLeadTime`                                     | object        |                                                |
| `averageLeadTime.unit`                                | string        | days                                           |
| `averageLeadTime.value`                               | integer       | 10                                             |
| `awards`                                              | array<object> | array (empty)                                  |                          |
| `awards[].image`                                      | object        |                                                |
| `awards[].image.alt`                                  | string        | Best Manufacturer Award                        |
| `awards[].image.exten`                                | string        | png                                            |
| `awards[].image.size`                                 | integer       | 896000                                         |
| `awards[].image.src`                                  | string        | https://www.example.com/award1.png             |
| `awards[].name`                                       | string        | Best Manufacturer 2023                         |
| `awards[].year`                                       | integer       | 2023                                           |
| `brochures`                                           | array<object> | array (empty)                                  |                          |
| `brochures[].alt`                                     | string        | assets/fSRxOPN5JG2NrwX09ZEqn.pdf               |
| `brochures[].exten`                                   | string        | application/pdf                                |
| `brochures[].size`                                    | integer       | 28117                                          |
| `brochures[].src`                                     | string        | assets/fSRxOPN5JG2NrwX09ZEqn.pdf               |
| `businessAddress`                                     | object        |                                                |
| `businessAddress.addressLine`                         | string        | 123 MG Road                                    |
| `businessAddress.city`                                | string        | Bangalore                                      |
| `businessAddress.country`                             | object        |                                                |
| `businessAddress.country.code`                        | string        | IN                                             |
| `businessAddress.country.name`                        | string        | India                                          |
| `businessAddress.pinCode`                             | string        | integer                                        | 560001                   |
| `businessAddress.pincode`                             | string        | 654321                                         |
| `businessAddress.state`                               | string        | Karnataka                                      |
| `businessEmail`                                       | string        | info@abcexports.com                            |
| `businessLocation`                                    | object        |                                                |
| `businessLocation.code`                               | string        | DE                                             |
| `businessLocation.name`                               | string        | Germany                                        |
| `businessName`                                        | string        | vel logistics Pvt Ltd                          |
| `businessPhoneNo`                                     | string        | object                                         | +91-9876543210           |
| `businessPhoneNo.countryCode`                         | string        | +91                                            |
| `businessPhoneNo.number`                              | string        | 9888888888                                     |
| `businessTaxInfo`                                     | array<object> | array (empty)                                  |                          |
| `businessTaxInfo[].taxes`                             | array<object> |                                                |
| `businessTaxInfo[].taxes[].country`                   | string        | India                                          |
| `businessTaxInfo[].taxes[].currency`                  | string        | INR                                            |
| `businessTaxInfo[].taxes[].default_tax_rates`         | string        | 5                                              |
| `businessTaxInfo[].taxes[].tax_id_label`              | string        | GSTIN                                          |
| `businessTaxInfo[].taxes[].tax_types`                 | string        | GST                                            |
| `businessType`                                        | string        | register                                       |
| `businessTypeSpecific`                                | string        | array (empty)                                  | array<string>            | Manufacturer |
| `certificates`                                        | array<object> | array (empty)                                  |                          |
| `certificates[].image`                                | object        |                                                |
| `certificates[].image.alt`                            | string        | ISO 9001:2015 Certification                    |
| `certificates[].image.exten`                          | string        | png                                            |
| `certificates[].image.size`                           | integer       | 1280000                                        |
| `certificates[].image.src`                            | string        | https://www.example.com/iso-cert.png           |
| `certificates[].name`                                 | string        | ISO 9001:2015                                  |
| `companyLogo`                                         | object        |                                                |
| `companyLogo.alt`                                     | string        | assets/t21dk0r_xfEZaBCPFyTUP.png               |
| `companyLogo.exten`                                   | string        | image/png                                      |
| `companyLogo.size`                                    | integer       | 1541                                           |
| `companyLogo.src`                                     | string        | assets/t21dk0r_xfEZaBCPFyTUP.png               |
| `companyRegisterNumber`                               | string        | REG1234567                                     |
| `companyVideo`                                        | object        |                                                |
| `companyVideo.alt`                                    | string        | Front view of the product                      |
| `companyVideo.exten`                                  | string        | jpg                                            |
| `companyVideo.size`                                   | integer       | 204800                                         |
| `companyVideo.src`                                    | string        | https://example.com/image.jpg                  |
| `companyVideoLink`                                    | string        | https://www.youtube.com/watch?v=example123     |
| `contractManufacturing`                               | array<string> |                                                |
| `createdAt`                                           | date          |                                                |
| `createdBy`                                           | string        | ObjectId                                       | 685e356012c0e23e441a681d |
| `dataPrivacySettings`                                 | object        |                                                |
| `dataPrivacySettings.consentToProcessData`            | boolean       | True                                           |
| `dataPrivacySettings.dataForAnalytics`                | boolean       | True                                           |
| `dataPrivacySettings.shareWithTrustedPartners`        | boolean       | True                                           |
| `deliveryTerm`                                        | array (empty) | array<string>                                  |                          |
| `exportPercent`                                       | integer       | 50                                             |
| `factoryDivision`                                     | array<object> | array (empty)                                  |                          |
| `factoryDivision[].address`                           | object        |                                                |
| `factoryDivision[].address.addressLine`               | string        | 123 Main St                                    |
| `factoryDivision[].address.city`                      | string        | Chennai                                        |
| `factoryDivision[].address.country`                   | object        |                                                |
| `factoryDivision[].address.country.code`              | string        | IN                                             |
| `factoryDivision[].address.country.name`              | string        | India                                          |
| `factoryDivision[].address.pinCode`                   | string        | 600001                                         |
| `factoryDivision[].address.state`                     | string        | Tamil Nadu                                     |
| `factoryDivision[].businessAddress`                   | object        |                                                |
| `factoryDivision[].businessAddress.addressLine`       | string        | 789 Factory Zone                               |
| `factoryDivision[].businessAddress.city`              | string        | Bangalore                                      |
| `factoryDivision[].businessAddress.country`           | object        |                                                |
| `factoryDivision[].businessAddress.country.code`      | string        | IN                                             |
| `factoryDivision[].businessAddress.country.name`      | string        | India                                          |
| `factoryDivision[].businessAddress.pinCode`           | string        | 560001                                         |
| `factoryDivision[].businessAddress.state`             | string        | Karnataka                                      |
| `factoryDivision[].companyName`                       | string        | Pepagora Manufacturing Pvt Ltd                 |
| `factoryDivision[].contactName`                       | string        | Arun Kumar                                     |
| `factoryDivision[].divisionName`                      | string        | Electrical Components Division                 |
| `factoryDivision[].googleMapLink`                     | string        | https://goo.gl/maps/xyz123                     |
| `factoryDivision[].phoneNumber`                       | string        | object                                         | 9876543210               |
| `factoryDivision[].phoneNumber.countryCode`           | string        | 91                                             |
| `factoryDivision[].phoneNumber.number`                | string        | 5434534543                                     |
| `gstNo`                                               | string        | gst-98986y87                                   |
| `iecDoc`                                              | object        |                                                |
| `iecDoc.alt`                                          | string        | assets/-SrR8aTL28n-ZY2e675Q8.pdf               |
| `iecDoc.exten`                                        | string        | application/pdf                                |
| `iecDoc.size`                                         | integer       | 142786                                         |
| `iecDoc.src`                                          | string        | assets/-SrR8aTL28n-ZY2e675Q8.pdf               |
| `iecNumber`                                           | string        | 7895412                                        |
| `industry`                                            | array<object> | array (empty)                                  | object                   |              |
| `industry._id`                                        | string        | 67f76dccf90b509ffc2f69aa                       |
| `industry.name`                                       | string        | Food                                           |
| `industry.uniqueId`                                   | string        | CAc92f6ff90f                                   |
| `industry[]._id`                                      | string        | 67f514f976706f860309ebeb                       |
| `industry[].name`                                     | string        | Fashion                                        |
| `industry[].uniqueId`                                 | string        | CA6c3cab3c96                                   |
| `infrastructureImg`                                   | array<object> | array (empty)                                  |                          |
| `infrastructureImg[].alt`                             | string        | Front view of the product                      |
| `infrastructureImg[].exten`                           | string        | jpg                                            |
| `infrastructureImg[].name`                            | string        | Factory Building                               |
| `infrastructureImg[].size`                            | integer       | 204800                                         |
| `infrastructureImg[].src`                             | string        | https://example.com/image.jpg                  |
| `infrastructureImg[].url`                             | string        | https://www.example.com/infrastructure.jpg     |
| `infrastructureOverview`                              | string        | Infrastructure overview description            |
| `kybVerification`                                     | object        |                                                |
| `kybVerification.businessAddressProof`                | object        |                                                |
| `kybVerification.businessAddressProof.document`       | object        |                                                |
| `kybVerification.businessAddressProof.document.alt`   | string        | assets/fgGIYxsxOuscdtqpMBX4p.png               |
| `kybVerification.businessAddressProof.document.exten` | string        | image/png                                      |
| `kybVerification.businessAddressProof.document.size`  | integer       | 41696                                          |
| `kybVerification.businessAddressProof.document.src`   | string        | assets/fgGIYxsxOuscdtqpMBX4p.png               |
| `kybVerification.businessAddressProof.documentType`   | string        | Pancard                                        |
| `kybVerification.businessRegistration`                | object        |                                                |
| `kybVerification.businessRegistration.documentId`     | string        | 851212809284                                   |
| `kybVerification.businessRegistration.documentType`   | string        | Aadhar                                         |
| `kybVerification.taxIdVerification`                   | object        |                                                |
| `kybVerification.taxIdVerification.document`          | object        |                                                |
| `kybVerification.taxIdVerification.document.alt`      | string        | assets/fkXBux4bIEU272LhruQ-s.png               |
| `kybVerification.taxIdVerification.document.exten`    | string        | image/png                                      |
| `kybVerification.taxIdVerification.document.size`     | integer       | 41696                                          |
| `kybVerification.taxIdVerification.document.src`      | string        | assets/fkXBux4bIEU272LhruQ-s.png               |
| `kybVerification.taxIdVerification.documentType`      | string        | Aadharcard                                     |
| `kycStatus`                                           | string        | Pending                                        |
| `kycVerification`                                     | object        |                                                |
| `kycVerification.addressVerification`                 | object        |                                                |
| `kycVerification.addressVerification.document`        | object        |                                                |
| `kycVerification.addressVerification.document.alt`    | string        | assets/Um9IC8XCigagLeT0TsoSy.pdf               |
| `kycVerification.addressVerification.document.exten`  | string        | application/pdf                                |
| `kycVerification.addressVerification.document.size`   | integer       | 5195548                                        |
| `kycVerification.addressVerification.document.src`    | string        | assets/Um9IC8XCigagLeT0TsoSy.pdf               |
| `kycVerification.addressVerification.documentType`    | string        | Pancard                                        |
| `kycVerification.identityVerification`                | object        |                                                |
| `kycVerification.identityVerification.document`       | object        |                                                |
| `kycVerification.identityVerification.document.alt`   | string        | assets/ZgE56bFPnMVkhkTCARhEf.jpg               |
| `kycVerification.identityVerification.document.exten` | string        | image/jpeg                                     |
| `kycVerification.identityVerification.document.size`  | integer       | 22817                                          |
| `kycVerification.identityVerification.document.src`   | string        | assets/ZgE56bFPnMVkhkTCARhEf.jpg               |
| `kycVerification.identityVerification.documentType`   | string        | Aadharcard                                     |
| `languageSpoken`                                      | array (empty) | array<string>                                  |                          |
| `legalBusinessName`                                   | string        | ABC Exports Pvt. Ltd.                          |
| `legalOwnerName`                                      | string        | Velu                                           |
| `legalStatus`                                         | string        | register                                       |
| `mainMarkets`                                         | array<object> |                                                |
| `mainMarkets[].code`                                  | string        | IN                                             |
| `mainMarkets[].name`                                  | string        | India                                          |
| `mainProducts`                                        | array (empty) | array<string>                                  |                          |
| `minOrderValue`                                       | object        |                                                |
| `minOrderValue.currency`                              | object        |                                                |
| `minOrderValue.currency.code`                         | string        | USD                                            |
| `minOrderValue.currency.name`                         | string        | United States Dollar                           |
| `minOrderValue.currency.symbol`                       | string        | $                                              |
| `minOrderValue.value`                                 | integer       | 500                                            |
| `mobileNumber`                                        | string        | 9876543210                                     |
| `msmeNo`                                              | string        |                                                |
| `nearestPort`                                         | string        | Poombuhar                                      |
| `noOfEmployees`                                       | string        | 1-10                                           |
| `noOfProductionLines`                                 | integer       | 3                                              |
| `noOfQcStaff`                                         | string        | integer                                        | 10                       |
| `noOfRdStaff`                                         | string        | integer                                        | 5                        |
| `otherBrands`                                         | array<object> | array (empty)                                  |                          |
| `otherBrands[].image`                                 | object        |                                                |
| `otherBrands[].image.alt`                             | string        | Partner Brand X Logo                           |
| `otherBrands[].image.exten`                           | string        | png                                            |
| `otherBrands[].image.size`                            | integer       | 640000                                         |
| `otherBrands[].image.src`                             | string        | https://www.example.com/partner-brand-x.png    |
| `otherBrands[].name`                                  | string        | Partner Brand X                                |
| `otherPaymentMethod`                                  | string        | UPI                                            |
| `ownBrands`                                           | array<object> | array (empty)                                  |                          |
| `ownBrands[].image`                                   | object        |                                                |
| `ownBrands[].image.alt`                               | string        | Brand A Logo                                   |
| `ownBrands[].image.exten`                             | string        | png                                            |
| `ownBrands[].image.size`                              | integer       | 512000                                         |
| `ownBrands[].image.src`                               | string        | https://www.example.com/brand-a-logo.png       |
| `ownBrands[].name`                                    | string        | Brand A                                        |
| `paymentMethods`                                      | array (empty) | array<string>                                  |                          |
| `paymentTerms`                                        | string        | ADVANCE_100                                    |
| `productBrief`                                        | string        | dadsad                                         |
| `productionFacilities`                                | string        | Automated assembly lines, quality control labs |
| `shippingAddress`                                     | object        |                                                |
| `shippingAddress.addressLine`                         | string        | 141                                            |
| `shippingAddress.city`                                | string        | Coimbatore                                     |
| `shippingAddress.country`                             | object        |                                                |
| `shippingAddress.country.code`                        | string        | IN                                             |
| `shippingAddress.country.name`                        | string        | India                                          |
| `shippingAddress.pinCode`                             | string        | 641001                                         |
| `shippingAddress.state`                               | string        | Tamil Nadu                                     |
| `shippingMethod`                                      | array (empty) | array<string>                                  |                          |
| `socialMediaLinks`                                    | object        |                                                |
| `socialMediaLinks.facebook`                           | string        |                                                |
| `socialMediaLinks.instagram`                          | string        |                                                |
| `socialMediaLinks.linkedin`                           | string        |                                                |
| `socialMediaLinks.youtube`                            | string        |                                                |
| `stageStatus`                                         | object        |                                                |
| `stageStatus.Additional`                              | string        | active                                         |
| `stageStatus.AdditionalFactoryDetails`                | string        | pending                                        |
| `stageStatus.AdditionalTradeDetails`                  | string        | pending                                        |
| `stageStatus.BrandingMedia`                           | string        | pending                                        |
| `stageStatus.BusinessDetails`                         | string        | active                                         |
| `stageStatus.CompanyRegistrationDetails`              | string        | active                                         |
| `stageStatus.FactoryWarehouseDetails`                 | string        | active                                         |
| `stageStatus.MarketLogistics`                         | string        | pending                                        |
| `stageStatus.ShippingPaymentTerms`                    | string        | pending                                        |
| `stageStatus.TaxIdentityVerification`                 | string        | active                                         |
| `timeZone`                                            | string        | Asia/Kolkata                                   |
| `totalFactorySize`                                    | string        | Below 1000 sqm                                 |
| `updatedAt`                                           | date          |                                                |
| `updatedBy`                                           | string        | ObjectId                                       | 685b8a51a8f68cc8e3c2008a |
| `warehouseCertification`                              | object        |                                                |
| `warehouseCertification.alt`                          | string        | Front view of the product                      |
| `warehouseCertification.exten`                        | string        | jpg                                            |
| `warehouseCertification.name`                         | string        | ISO 9001                                       |
| `warehouseCertification.size`                         | integer       | 204800                                         |
| `warehouseCertification.src`                          | string        | https://example.com/image.jpg                  |
| `warehouseCertification.url`                          | string        | https://www.example.com/cert.jpg               |
| `warehouseStorageArea`                                | string        | <1000 sqft                                     |
| `website`                                             | string        | https://abcexports.com                         |
| `yearOfEstablishment`                                 | integer       | 2012                                           |

### First Document (sanitized)

```json
{
  "_id": "687c6a7d36d833cdf68e0f6b",
  "createdBy": "685e3e9a909298eae0b63672",
  "legalBusinessName": "Pepagora Enterprises",
  "businessName": "Pepagora Pvt Ltd",
  "businessAddress": {
    "addressLine": "123 Business Street",
    "city": "Chennai",
    "state": "Tamil Nadu",
    "pinCode": "600001",
    "country": {
      "name": "India",
      "code": "IN"
    }
  },
  "legalOwnerName": "JohnDoe",
  "legalStatus": "register",
  "businessType": "Manufacturer",
  "mobileNumber": "9876543210",
  "businessEmail": "contact@pepagora.com",
  "industry": [
    {
      "_id": "64d3f7a25b4d2e3c72c81b2e",
      "name": "Electronics",
      "uniqueId": "industry-electronics"
    }
  ],
  "yearOfEstablishment": 2012,
  "noOfEmployees": "11–25",
  "mainProducts": ["LED Bulbs", "Cables", "Switches"],
  "stageStatus": {
    "BusinessDetails": "completed",
    "CompanyRegistrationDetails": "completed",
    "TaxIdentityVerification": "completed",
    "FactoryWarehouseDetails": "completed",
    "Additional": "completed",
    "BrandingMedia": "completed",
    "MarketLogistics": "completed",
    "ShippingPaymentTerms": "completed",
    "AdditionalTradeDetails": "completed"
  },
  "createdAt": "2025-07-20T04:03:09.772000",
  "updatedAt": "2025-07-20T08:27:35.054000",
  "__v": 0,
  "updatedBy": "685e3e9a909298eae0b63672",
  "companyRegisterNumber": "REG1234567",
  "gstNo": "gst-98986y87",
  "contractManufacturing": ["OEM Service"],
  "annualOutputValue": "Less than $1M",
  "annualTurnover": "Below ₹25 Lakhs",
  "infrastructureImg": [
    {
      "url": "https://www.example.com/infrastructure.jpg",
      "name": "Factory Building"
    }
  ],
  "infrastructureOverview": "Modern infrastructure with advanced machinery and safety standards.",
  "noOfProductionLines": 3,
  "noOfQcStaff": "10",
  "noOfRdStaff": "5",
  "productionFacilities": "Automated assembly lines, quality control labs",
  "shippingAddress": {
    "addressLine": "123 Business Street",
    "city": "Chennai",
    "state": "Tamil Nadu",
    "pinCode": "600001",
    "country": {
      "name": "India",
      "code": "IN"
    }
  },
  "totalFactorySize": "Below 1000 sqm",
  "warehouseCertification": {
    "url": "https://www.example.com/cert.jpg",
    "name": "ISO 9001"
  },
  "warehouseStorageArea": "<1000 sqft",
  "website": "https://www.example.com",
  "factoryDivision": [
    {
      "divisionName": "Electrical Components Division",
      "companyName": "Pepagora Manufacturing Pvt Ltd",
      "contactName": "Arun Kumar",
      "phoneNumber": "9876543210",
      "businessAddress": {
        "addressLine": "789 Factory Zone",
        "city": "Bangalore",
        "state": "Karnataka",
        "pinCode": "560001",
        "country": {
          "name": "India",
          "code": "IN"
        }
      },
      "googleMapLink": "https://goo.gl/maps/xyz123"
    }
  ],
  "awards": [
    {
      "name": "Best Manufacturer 2023",
      "image": {
        "src": "https://www.example.com/award1.png",
        "alt": "Best Manufacturer Award",
        "exten": "png",
        "size": 896000
      },
      "year": 2023
    },
    {
      "name": "Quality Excellence Award",
      "image": {
        "src": "https://www.example.com/award2.png",
        "alt": "Quality Excellence Award",
        "exten": "png",
        "size": 1024000
      },
      "year": 2022
    }
  ],
  "brochures": [
    {
      "src": "https://www.example.com/brochure1.pdf",
      "alt": "Product Brochure 2024",
      "exten": "pdf",
      "size": 2048000
    },
    {
      "src": "https://www.example.com/brochure2.pdf",
      "alt": "Company Profile",
      "exten": "pdf",
      "size": 1536000
    }
  ],
  "certificates": [
    {
      "name": "ISO 9001:2015",
      "image": {
        "src": "https://www.example.com/iso-cert.png",
        "alt": "ISO 9001:2015 Certification",
        "exten": "png",
        "size": 1280000
      }
    }
  ],
  "companyLogo": {
    "src": "https://www.example.com/logo.png",
    "alt": "Company Logo",
    "exten": "png",
    "size": 1024000
  },
  "companyVideoLink": "https://www.youtube.com/watch?v=example123",
  "otherBrands": [
    {
      "name": "Partner Brand X",
      "image": {
        "src": "https://www.example.com/partner-brand-x.png",
        "alt": "Partner Brand X Logo",
        "exten": "png",
        "size": 640000
      }
    }
  ],
  "ownBrands": [
    {
      "name": "Brand A",
      "image": {
        "src": "https://www.example.com/brand-a-logo.png",
        "alt": "Brand A Logo",
        "exten": "png",
        "size": 512000
      }
    },
    {
      "name": "Brand B",
      "image": {
        "src": "https://www.example.com/brand-b-logo.png",
        "alt": "Brand B Logo",
        "exten": "png",
        "size": 768000
      }
    }
  ],
  "socialMediaLinks": {
    "facebook": "https://www.facebook.com/companyname",
    "youtube": "https://www.youtube.com/@companyname",
    "instagram": "https://www.instagram.com/companyname",
    "linkedin": "https://www.linkedin.com/company/companyname"
  },
  "mainMarkets": [
    {
      "name": "India",
      "code": "IN"
    },
    {
      "name": "United States",
      "code": "US"
    }
  ],
  "acceptedCurrency": [
    {
      "code": "INR",
      "name": "Indian Rupee",
      "symbol": "₹"
    },
    {
      "code": "USD",
      "name": "US Dollar",
      "symbol": "$"
    }
  ],
  "paymentMethods": ["credit", "paypal", "cash"],
  "paymentTerms": "ADVANCE_100",
  "shippingMethod": ["Sea", "Air", "Courier"],
  "averageLeadTime": {
    "value": 14,
    "unit": "days"
  },
  "exportPercent": 75,
  "iecDoc": {
    "src": "https://www.example.com/iec-doc.pdf",
    "alt": "IEC Document",
    "exten": "pdf",
    "size": 204800
  },
  "iecNumber": "ABCD1234567E",
  "languageSpoken": ["English", "Hindi", "Tamil"],
  "minOrderValue": {
    "currency": {
      "code": "INR",
      "name": "Indian Rupee",
      "symbol": "₹"
    },
    "value": 10000
  },
  "nearestPort": "Chennai Port"
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

**createdBy_1**

- Type: Unique
- Keys:
  - `createdBy`: ascending

---

## buyingrequests

**Document Count:** 177
**Sample Size:** 100

### Fields

| Field                                    | Type          | Example                                           |
| ---------------------------------------- | ------------- | ------------------------------------------------- | --- |
| `__v`                                    | integer       | 0                                                 |
| `_id`                                    | ObjectId      |                                                   |
| `additionalBuyingReqDetails`             | string        | tsetsetsfsdf sdf                                  |
| `analytics`                              | object        |                                                   |
| `analytics._id`                          | ObjectId      |                                                   |
| `analytics.impressions`                  | integer       | 0                                                 |
| `analytics.quotesReceivedCount`          | integer       | 0                                                 |
| `analytics.views`                        | integer       | 0                                                 |
| `annualPurchaseVolume`                   | object        |                                                   |
| `annualPurchaseVolume.max`               | string        | 50000                                             |
| `annualPurchaseVolume.min`               | string        | 10000                                             |
| `assignTo`                               | ObjectId      |                                                   |
| `cartId`                                 | ObjectId      |                                                   |
| `category`                               | object        |                                                   |
| `category._id`                           | string        | 67f514f976706f860309ebeb                          |
| `category.name`                          | string        | Fashion                                           |
| `category.uniqueId`                      | string        | CA4fd69f0a69                                      |
| `categorySuggestion`                     | object        |                                                   |
| `categorySuggestion.industry`            | string        | Technology                                        |
| `categorySuggestion.reason`              | string        |                                                   |
| `categorySuggestion.suggestedCategory`   | string        | Smart Wearables                                   |
| `createdAt`                              | date          |                                                   |
| `createdBy`                              | ObjectId      |                                                   |
| `currency`                               | object        |                                                   |
| `currency.code`                          | string        | INR                                               |
| `currency.name`                          | string        | Indian Rupee                                      |
| `currency.symbol`                        | string        | ₹                                                 |
| `customizationRequired`                  | boolean       | False                                             |
| `destinationPort`                        | string        | Port of LA                                        |
| `estOrderQuantity`                       | integer       | object                                            | 0   |
| `estOrderQuantity.quantity`              | integer       | 188                                               |
| `estOrderQuantity.unit`                  | string        | pieces                                            |
| `expectedDeliveryTime`                   | string        | Express                                           |
| `hasVariants`                            | boolean       | False                                             |
| `isApproved`                             | boolean       | True                                              |
| `isArchived`                             | boolean       | False                                             |
| `isDraft`                                | boolean       | True                                              |
| `isRejected`                             | boolean       | False                                             |
| `leads`                                  | array (empty) |                                                   |
| `offerInfo`                              | object        |                                                   |
| `offerInfo.currency`                     | object        |                                                   |
| `offerInfo.currency.code`                | string        | INR                                               |
| `offerInfo.currency.name`                | string        | Indian Rupee                                      |
| `offerInfo.currency.symbol`              | string        | ₹                                                 |
| `offerInfo.discountPercent`              | integer       | 25                                                |
| `offerInfo.maxQty`                       | integer       | 100                                               |
| `offerInfo.minQty`                       | integer       | 55                                                |
| `offerInfo.offerType`                    | string        | fixedDiscount                                     |
| `offerInfo.pricing`                      | object        |                                                   |
| `offerInfo.pricing.bulkPrices`           | array<object> |                                                   |
| `offerInfo.pricing.bulkPrices[].maxQty`  | integer       | 200                                               |
| `offerInfo.pricing.bulkPrices[].minQty`  | integer       | 100                                               |
| `offerInfo.pricing.bulkPrices[].price`   | integer       | 375                                               |
| `offerInfo.pricing.pricingType`          | string        | bulk                                              |
| `offerInfo.pricing.unit`                 | string        | pieces                                            |
| `offerInfo.pricing.unitPrice`            | number        | 0.35                                              |
| `offerInfo.unit`                         | string        | pieces                                            |
| `paymentTerms`                           | string        | Net 30                                            |
| `preferredSourcingRegion`                | string        | Nearby                                            |
| `preferredUnitPrice`                     | object        |                                                   |
| `preferredUnitPrice.currency`            | object        |                                                   |
| `preferredUnitPrice.currency.code`       | string        | INR                                               |
| `preferredUnitPrice.currency.name`       | string        | Indian Rupee                                      |
| `preferredUnitPrice.currency.symbol`     | string        | ₹                                                 |
| `preferredUnitPrice.priceRange`          | object        |                                                   |
| `preferredUnitPrice.priceRange.maxPrice` | integer       | 8000                                              |
| `preferredUnitPrice.priceRange.minPrice` | integer       | 500                                               |
| `pricing`                                | object        |                                                   |
| `pricing.bulkPrices`                     | array<object> |                                                   |
| `pricing.bulkPrices[].maxQty`            | integer       | 500                                               |
| `pricing.bulkPrices[].minQty`            | integer       | 100                                               |
| `pricing.bulkPrices[].price`             | integer       | 10000                                             |
| `pricing.maxPrice`                       | integer       | 150                                               |
| `pricing.minPrice`                       | integer       | 100                                               |
| `pricing.pricingType`                    | string        | fixed                                             |
| `pricing.unit`                           | string        | pieces                                            |
| `pricing.unitPrice`                      | integer       | 10                                                |
| `productCategory`                        | object        |                                                   |
| `productCategory._id`                    | string        | 67f5124876706f860309ebd3                          |
| `productCategory.name`                   | string        | Shirts                                            |
| `productDescription`                     | string        | This is a sample product description for testing. |
| `productId`                              | ObjectId      |                                                   |
| `productImage`                           | array<object> |                                                   |
| `productImage[].alt`                     | string        | White Organic Cotton T-Shirt                      |
| `productImage[].exten`                   | string        | jpg                                               |
| `productImage[].size`                    | integer       | 204800                                            |
| `productImage[].src`                     | string        | https://example.com/images/tshirt.jpg             |
| `productName`                            | string        | black saree                                       |
| `quotesReceived`                         | array (empty) |                                                   |
| `rfqDescription`                         | string        | <p>test</p>                                       |
| `rfqId`                                  | string        | RFQ85fd42fd96                                     |
| `rfqTitle`                               | string        | Mange Tout Gifts Trading LLC                      |
| `sampleRequired`                         | boolean       | False                                             |
| `selectedVariants`                       | array<object> | array (empty)                                     |     |
| `selectedVariants[]._id`                 | string        | 68591ab1bba19d77016ac06e                          |
| `selectedVariants[].quantity`            | integer       | 50                                                |
| `shippingMethod`                         | array<string> |                                                   |
| `sourcingFrequency`                      | string        | Monthly                                           |
| `status`                                 | string        | Approval Pending                                  |
| `subCategory`                            | object        |                                                   |
| `subCategory._id`                        | string        | 67f515a076706f860309ebf4                          |
| `subCategory.name`                       | string        | Mobile Phonesdfs                                  |
| `subCategory.uniqueId`                   | string        | SC80ef757705                                      |
| `supplierId`                             | ObjectId      |                                                   |
| `supplyContractType`                     | string        | One Year Contract                                 |
| `totalOrderQuantity`                     | integer       | 200                                               |
| `type`                                   | string        | BR                                                |
| `updatedAt`                              | date          |                                                   |
| `validityDate`                           | date          |                                                   |

### First Document (sanitized)

```json
{
  "_id": "685640018d6f9aa326d1d99d",
  "productName": "Shoe",
  "createdBy": "685b89a6a8f68cc8e3c20069",
  "productDescription": "Step into comfort and style with our versatile Shoe. Designed for all-day wear, it offers optimal support and a sleek look. Perfect for any occasion, its durable material ensures long-lasting use. Elevate your footwear collection today!",
  "category": {
    "_id": "67f514f976706f860309ebeb",
    "name": "Fashion",
    "uniqueId": "CA6c3cab3c96"
  },
  "subCategory": {
    "_id": "67f515a976706f860309ebf5",
    "name": "sports",
    "uniqueId": "SC6e16b67695"
  },
  "productCategory": {
    "_id": "67f5124876706f860309ebd7",
    "name": "Watches"
  },
  "estOrderQuantity": 0,
  "preferredSourcingRegion": "Nearby",
  "sampleRequired": false,
  "customizationRequired": false,
  "rfqId": "RFQ16d64f823a",
  "type": "RFQ",
  "status": "Quotes Received",
  "quotesReceived": [],
  "leads": [],
  "analytics": {
    "impressions": 0,
    "views": 0,
    "quotesReceivedCount": 0,
    "_id": "6864d1f79f4724a44f26e442"
  },
  "isArchived": false,
  "isApproved": true,
  "isDraft": true,
  "productId": "685640018d6f9aa326d1d99d",
  "selectedVariants": [
    {
      "_id": "68591ab1bba19d77016ac06e",
      "quantity": 23
    }
  ],
  "rfqDescription": "avx",
  "totalOrderQuantity": 23,
  "hasVariants": true,
  "createdAt": "2025-06-20T11:59:42.273000",
  "__v": 0,
  "updatedAt": "2025-07-11T12:27:07.450000",
  "isRejected": false
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## catalog_datas

**Document Count:** 2
**Sample Size:** 2

### Fields

| Field                   | Type          | Example                  |
| ----------------------- | ------------- | ------------------------ | ------- |
| `__v`                   | integer       | 1                        |
| `_id`                   | ObjectId      |                          |
| `analytics`             | object        |                          |
| `analytics.shares`      | integer       | 0                        |
| `analytics.views`       | integer       | 0                        |
| `businessType`          | string        | unregister               |
| `businessTypeSpecific`  | array<string> |                          |
| `catalogStage`          | object        |                          |
| `catalogStage.homepage` | string        | completed                |
| `catalogStage.products` | string        | completed                |
| `createdAt`             | date          |                          |
| `createdBy`             | ObjectId      |                          |
| `impression`            | integer       | 0                        |
| `impressionIPs`         | array (empty) |                          |
| `industry`              | string        | object                   | apparel |
| `industry._id`          | string        | 67f76dccf90b509ffc2f69aa |
| `industry.liveUrl`      | string        | Food_CAc92f6ff90f        |
| `industry.name`         | string        | Food                     |
| `industry.uniqueId`     | string        | CAc92f6ff90f             |
| `isCatalogPublished`    | boolean       | False                    |
| `ownerName`             | string        | ABC Pvt Ltd              |
| `productIds`            | array (empty) |                          |
| `status`                | string        | pending                  |
| `subDomain`             | string        | abc-store                |
| `updatedAt`             | date          |                          |
| `viewedIPs`             | array<object> |                          |
| `viewedIPs[]._id`       | ObjectId      |                          |
| `viewedIPs[].ip`        | string        | ::1                      |
| `viewedIPs[].viewedAt`  | date          |                          |
| `views`                 | integer       | 1                        |

### First Document (sanitized)

```json
{
  "_id": "6897645b76676e0e802f0392",
  "subDomain": "palpx",
  "createdBy": "6868e10b3369cbe111a62ce3",
  "ownerName": "palpx",
  "businessTypeSpecific": ["Manufacturer"],
  "businessType": "register",
  "industry": "apparel",
  "status": "pending",
  "productIds": [],
  "analytics": {
    "views": 0,
    "shares": 0
  },
  "catalogStage": {
    "homepage": "completed",
    "products": "completed"
  },
  "createdAt": "2025-08-09T15:08:11.561000",
  "updatedAt": "2025-08-09T15:22:58.116000",
  "__v": 0
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

**subDomain_1**

- Type: Unique
- Keys:
  - `subDomain`: ascending

---

## catalogs

**Document Count:** 16
**Sample Size:** 16

### Fields

| Field | Type     | Example |
| ----- | -------- | ------- |
| `__v` | integer  | 0       |
| `_id` | ObjectId |         |

### First Document (sanitized)

```json
{
  "_id": "689733fb18678a09e7972508",
  "__v": 0
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## categories

**Document Count:** 5
**Sample Size:** 5

### Fields

| Field            | Type          | Example                  |
| ---------------- | ------------- | ------------------------ |
| `_id`            | ObjectId      |                          |
| `liveUrl`        | string        | Electronics_CAee40f0e5be |
| `mappedChildren` | array<string> |                          |
| `name`           | string        | Electronics              |
| `uniqueId`       | string        | CAee40f0e5be             |

### First Document (sanitized)

```json
{
  "_id": "67f514ee76706f860309ebe9",
  "uniqueId": "CAee40f0e5be",
  "liveUrl": "Electronics_CAee40f0e5be",
  "name": "Electronics",
  "mappedChildren": ["67f5154376706f860309ebf0", "67f5158976706f860309ebf3"]
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

**uniqueId_1**

- Type: Unique
- Keys:
  - `uniqueId`: ascending

**liveUrl_1**

- Type: Unique
- Keys:
  - `liveUrl`: ascending

---

## client_sessions

**Document Count:** 828
**Sample Size:** 100

### Fields

| Field              | Type     | Example                   |
| ------------------ | -------- | ------------------------- |
| `__v`              | integer  | 0                         |
| `_id`              | ObjectId |                           |
| `authSession`      | string   |                           |
| `countryCode`      | string   | +91                       |
| `createdAt`        | date     |                           |
| `email`            | string   | pepagora.betaqa@gmail.com |
| `emailOtpVerified` | boolean  | True                      |
| `expiry_date`      | date     |                           |
| `isVerifiedUser`   | boolean  | True                      |
| `phoneNo`          | string   | 9597362973                |
| `phoneOtpVerified` | boolean  | False                     |
| `updatedAt`        | date     |                           |

### First Document (sanitized)

```json
{
  "_id": "685b805feb6995d34ef05be3",
  "emailOtpVerified": true,
  "phoneOtpVerified": true,
  "expiry_date": "2025-06-25T04:56:43.614000",
  "authSession": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleGlzdGluZ1VzZXIiOmZhbHNlLCJlbWFpbCI6InVtYXByZWV0aGkuc0Bzb2x1dGlvbmNoYW1wcy5jb20iLCJpYXQiOjE3NTA4MjcxMDMsImV4cCI6MTc1MzQxOTEwM30.Ra7WPxxfqdPVjFN58UeSRJKzbebquaj4YQckduQ6e4E",
  "email": "umapreethi.s@solutionchamps.com",
  "isVerifiedUser": false,
  "createdAt": "2025-06-25T04:51:43.629000",
  "updatedAt": "2025-06-25T04:54:07.742000",
  "__v": 0,
  "countryCode": "+91",
  "phoneNo": "9940820162"
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## contents

**Document Count:** 0
**Sample Size:** 0

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## customers

**Document Count:** 205
**Sample Size:** 100

### Fields

| Field                 | Type            | Example                         |
| --------------------- | --------------- | ------------------------------- | ------------- |
| `__v`                 | integer         | 0                               |
| `_id`                 | ObjectId        |                                 |
| `companyName`         | string          | Braun Group                     |
| `contactName`         | string          | umapreethi.s                    |
| `country`             | string          | object                          | United States |
| `country.code`        | string          | IN                              |
| `country.name`        | string          | India                           |
| `createdAt`           | date            |                                 |
| `createdBy`           | ObjectId        |                                 |
| `email`               | string          | umapreethi.s@solutionchamps.com |
| `isArchived`          | boolean         | True                            |
| `isDraft`             | boolean         | False                           |
| `jobTitle`            | string          | Customer Web Supervisor         |
| `lastContactedAt`     | date            |                                 |
| `lifeCycle`           | string          | lead                            |
| `phoneNo`             | string          | 9940820162                      |
| `responses`           | object          |                                 |
| `responses.leads`     | array<ObjectId> | array (empty)                   |               |
| `responses.quoteIds`  | array (empty)   |                                 |
| `responses.threadIds` | array (empty)   | array<string>                   |               |
| `source`              | string          | Offline                         |
| `status`              | string          | active                          |
| `updatedAt`           | date            |                                 |
| `user_id`             | ObjectId        |                                 |
| `whatsAppNo`          | string          | 9861282119                      |

### First Document (sanitized)

```json
{
  "_id": "685b8a4e9801aeddc0807802",
  "contactName": "John Doe",
  "companyName": "Tech Solutions Inc.",
  "user_id": "685b8a4e9801aeddc0807803",
  "createdBy": "685b85aa523555fdc050e413",
  "email": "john.doe@example.com",
  "jobTitle": "Software Engineer",
  "phoneNo": "+1234567890",
  "whatsAppNo": "+1234567890",
  "source": "Website",
  "country": "United States",
  "lifeCycle": "lead",
  "status": "active",
  "createdAt": "2025-06-25T05:34:06.452000",
  "updatedAt": "2025-07-07T04:14:03.624000",
  "__v": 0,
  "responses": {
    "leads": [],
    "quoteIds": [],
    "threadIds": ["686b498bfd8fa1f0d6bd0d0b"]
  }
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## enquiries

**Document Count:** 4
**Sample Size:** 4

### Fields

| Field         | Type     | Example                       |
| ------------- | -------- | ----------------------------- |
| `__v`         | integer  | 0                             |
| `_id`         | ObjectId |                               |
| `catalogId`   | ObjectId |                               |
| `country`     | string   | india                         |
| `createdAt`   | date     |                               |
| `email`       | string   | ggf@dasd.com                  |
| `isResponded` | boolean  | False                         |
| `message`     | string   | asdasd as asdsd sadasd sad sd |
| `mobile`      | string   | 98467521305                   |
| `name`        | string   | velmurugan                    |
| `updatedAt`   | date     |                               |

### First Document (sanitized)

```json
{
  "_id": "6895f0ad65600997efc6eb33",
  "name": "John Doe",
  "email": "pepagora@example.com",
  "mobile": "876543210",
  "country": "India",
  "message": "Looking to source 500 units of PVC pipe, size 2 inches, with delivery in 10 days.",
  "catalogId": "6895d5913818ff4944141700",
  "isResponded": false,
  "createdAt": "2025-08-08T12:42:21.983000",
  "updatedAt": "2025-08-08T12:42:21.983000",
  "__v": 0
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## exchangerates

**Document Count:** 1
**Sample Size:** 1

### Fields

| Field           | Type    | Example                  |
| --------------- | ------- | ------------------------ |
| `__v`           | integer | 0                        |
| `_id`           | string  | singleton-exchange-rates |
| `createdAt`     | date    |                          |
| `quotes`        | object  |                          |
| `quotes.USDAED` | number  | 3.672985                 |
| `quotes.USDAFN` | number  | 68.232749                |
| `quotes.USDALL` | number  | 83.558715                |
| `quotes.USDAMD` | number  | 383.502854               |
| `quotes.USDANG` | number  | 1.789699                 |
| `quotes.USDAOA` | number  | 917.00015                |
| `quotes.USDARS` | number  | 1325.272673              |
| `quotes.USDAUD` | number  | 1.534295                 |
| `quotes.USDAWG` | number  | 1.8025                   |
| `quotes.USDAZN` | number  | 1.6975                   |
| `quotes.USDBAM` | number  | 1.678726                 |
| `quotes.USDBBD` | number  | 2.017189                 |
| `quotes.USDBDT` | number  | 121.342432               |
| `quotes.USDBGN` | number  | 1.677841                 |
| `quotes.USDBHD` | number  | 0.377014                 |
| `quotes.USDBIF` | number  | 2978.990118              |
| `quotes.USDBMD` | integer | 1                        |
| `quotes.USDBND` | number  | 1.283861                 |
| `quotes.USDBOB` | number  | 6.900991                 |
| `quotes.USDBRL` | number  | 5.431197                 |
| `quotes.USDBSD` | number  | 0.999064                 |
| `quotes.USDBTC` | number  | 8.203109e-06             |
| `quotes.USDBTN` | number  | 87.452899                |
| `quotes.USDBWP` | number  | 13.442146                |
| `quotes.USDBYN` | number  | 3.297455                 |
| `quotes.USDBYR` | integer | 19600                    |
| `quotes.USDBZD` | number  | 2.0068                   |
| `quotes.USDCAD` | number  | 1.37663                  |
| `quotes.USDCDF` | number  | 2889.999409              |
| `quotes.USDCHF` | number  | 0.807198                 |
| `quotes.USDCLF` | number  | 0.024681                 |
| `quotes.USDCLP` | number  | 968.209662               |
| `quotes.USDCNH` | number  | 7.18632                  |
| `quotes.USDCNY` | number  | 7.181498                 |
| `quotes.USDCOP` | number  | 4050.86                  |
| `quotes.USDCRC` | number  | 506.224779               |
| `quotes.USDCUC` | integer | 1                        |
| `quotes.USDCUP` | number  | 26.5                     |
| `quotes.USDCVE` | number  | 94.644007                |
| `quotes.USDCZK` | number  | 20.956033                |
| `quotes.USDDJF` | number  | 177.901416               |
| `quotes.USDDKK` | number  | 6.40227                  |
| `quotes.USDDOP` | number  | 61.011419                |
| `quotes.USDDZD` | number  | 129.902425               |
| `quotes.USDEGP` | number  | 48.429098                |
| `quotes.USDERN` | integer | 15                       |
| `quotes.USDETB` | number  | 138.627715               |
| `quotes.USDEUR` | number  | 0.85776                  |
| `quotes.USDFJD` | number  | 2.254898                 |
| `quotes.USDFKP` | number  | 0.743585                 |
| `quotes.USDGBP` | number  | 0.74297                  |
| `quotes.USDGEL` | number  | 2.701691                 |
| `quotes.USDGGP` | number  | 0.743585                 |
| `quotes.USDGHS` | number  | 10.536887                |
| `quotes.USDGIP` | number  | 0.743585                 |
| `quotes.USDGMD` | number  | 72.473275                |
| `quotes.USDGNF` | number  | 8663.249448              |
| `quotes.USDGTQ` | number  | 7.66319                  |
| `quotes.USDGYD` | number  | 208.952405               |
| `quotes.USDHKD` | number  | 7.849925                 |
| `quotes.USDHNL` | number  | 26.159526                |
| `quotes.USDHRK` | number  | 6.461703                 |
| `quotes.USDHTG` | number  | 130.72148                |
| `quotes.USDHUF` | number  | 338.792497               |
| `quotes.USDIDR` | number  | 16266.8                  |
| `quotes.USDILS` | number  | 3.41363                  |
| `quotes.USDIMP` | number  | 0.743585                 |
| `quotes.USDINR` | number  | 87.616203                |
| `quotes.USDIQD` | number  | 1308.355865              |
| `quotes.USDIRR` | number  | 42124.999512             |
| `quotes.USDISK` | number  | 122.630219               |
| `quotes.USDJEP` | number  | 0.743585                 |
| `quotes.USDJMD` | number  | 159.95604                |
| `quotes.USDJOD` | number  | 0.708995                 |
| `quotes.USDJPY` | number  | 147.562504               |
| `quotes.USDKES` | number  | 129.202654               |
| `quotes.USDKGS` | number  | 87.450101                |
| `quotes.USDKHR` | number  | 4001.940439              |
| `quotes.USDKMF` | number  | 422.150219               |
| `quotes.USDKPW` | number  | 900.000119               |
| `quotes.USDKRW` | number  | 1389.269868              |
| `quotes.USDKWD` | number  | 0.30553                  |
| `quotes.USDKYD` | number  | 0.832325                 |
| `quotes.USDKZT` | number  | 539.727909               |
| `quotes.USDLAK` | number  | 21608.514656             |
| `quotes.USDLBP` | number  | 89486.545642             |
| `quotes.USDLKR` | number  | 300.373375               |
| `quotes.USDLRD` | number  | 200.248916               |
| `quotes.USDLSL` | number  | 17.702931                |
| `quotes.USDLTL` | number  | 2.95274                  |
| `quotes.USDLVL` | number  | 0.604889                 |
| `quotes.USDLYD` | number  | 5.416892                 |
| `quotes.USDMAD` | number  | 9.044505                 |
| `quotes.USDMDL` | number  | 16.768379                |
| `quotes.USDMGA` | number  | 4408.879578              |
| `quotes.USDMKD` | number  | 52.719056                |
| `quotes.USDMMK` | number  | 2099.278286              |
| `quotes.USDMNT` | number  | 3593.667467              |
| `quotes.USDMOP` | number  | 8.075018                 |
| `quotes.USDMRU` | number  | 39.850605                |
| `quotes.USDMUR` | number  | 45.38004                 |
| `quotes.USDMVR` | number  | 15.403747                |
| `quotes.USDMWK` | number  | 1732.384873              |
| `quotes.USDMXN` | number  | 18.582685                |
| `quotes.USDMYR` | number  | 4.234027                 |
| `quotes.USDMZN` | number  | 63.959659                |
| `quotes.USDNAD` | number  | 17.702931                |
| `quotes.USDNGN` | number  | 1531.680479              |
| `quotes.USDNIO` | number  | 36.765148                |
| `quotes.USDNOK` | number  | 10.27799                 |
| `quotes.USDNPR` | number  | 139.966515               |
| `quotes.USDNZD` | number  | 1.682978                 |
| `quotes.USDOMR` | number  | 0.384507                 |
| `quotes.USDPAB` | number  | 0.998755                 |
| `quotes.USDPEN` | number  | 3.535041                 |
| `quotes.USDPGK` | number  | 4.213997                 |
| `quotes.USDPHP` | number  | 57.003045                |
| `quotes.USDPKR` | number  | 283.47835                |
| `quotes.USDPLN` | number  | 3.644066                 |
| `quotes.USDPYG` | number  | 7482.677794              |
| `quotes.USDQAR` | number  | 3.650401                 |
| `quotes.USDRON` | number  | 4.348968                 |
| `quotes.USDRSD` | number  | 100.467974               |
| `quotes.USDRUB` | number  | 79.875385                |
| `quotes.USDRWF` | number  | 1445.099361              |
| `quotes.USDSAR` | number  | 3.754749                 |
| `quotes.USDSBD` | number  | 8.217066                 |
| `quotes.USDSCR` | number  | 14.741998                |
| `quotes.USDSDG` | number  | 600.505228               |
| `quotes.USDSEK` | number  | 9.56741                  |
| `quotes.USDSGD` | number  | 1.284025                 |
| `quotes.USDSHP` | number  | 0.785843                 |
| `quotes.USDSLE` | number  | 23.098543                |
| `quotes.USDSLL` | number  | 20969.503947             |
| `quotes.USDSOS` | number  | 570.964931               |
| `quotes.USDSRD` | number  | 37.279032                |
| `quotes.USDSTD` | number  | 20697.981008             |
| `quotes.USDSTN` | number  | 21.03564                 |
| `quotes.USDSVC` | number  | 8.738681                 |
| `quotes.USDSYP` | number  | 13001.771596             |
| `quotes.USDSZL` | number  | 17.701706                |
| `quotes.USDTHB` | number  | 32.346502                |
| `quotes.USDTJS` | number  | 9.328183                 |
| `quotes.USDTMT` | number  | 3.51                     |
| `quotes.USDTND` | number  | 2.928973                 |
| `quotes.USDTOP` | number  | 2.342103                 |
| `quotes.USDTRY` | number  | 40.71665                 |
| `quotes.USDTTD` | number  | 6.779108                 |
| `quotes.USDTWD` | number  | 29.927496                |
| `quotes.USDTZS` | number  | 2475.00017               |
| `quotes.USDUAH` | number  | 41.327043                |
| `quotes.USDUGX` | number  | 3563.795545              |
| `quotes.USDUYU` | number  | 40.075533                |
| `quotes.USDUZS` | number  | 12578.000944             |
| `quotes.USDVES` | number  | 128.74775                |
| `quotes.USDVND` | number  | 26226.5                  |
| `quotes.USDVUV` | number  | 119.401149               |
| `quotes.USDWST` | number  | 2.653917                 |
| `quotes.USDXAF` | number  | 563.200666               |
| `quotes.USDXAG` | number  | 0.026317                 |
| `quotes.USDXAU` | number  | 0.000297                 |
| `quotes.USDXCD` | number  | 2.70255                  |
| `quotes.USDXCG` | number  | 1.800009                 |
| `quotes.USDXDR` | number  | 0.700441                 |
| `quotes.USDXOF` | number  | 563.203084               |
| `quotes.USDXPF` | number  | 102.364705               |
| `quotes.USDYER` | number  | 240.449827               |
| `quotes.USDZAR` | number  | 17.73076                 |
| `quotes.USDZMK` | number  | 9001.196527              |
| `quotes.USDZMW` | number  | 23.152942                |
| `quotes.USDZWL` | number  | 321.999592               |
| `source`        | string  | USD                      |
| `updatedAt`     | date    |                          |

### First Document (sanitized)

```json
{
  "_id": "singleton-exchange-rates",
  "source": "USD",
  "quotes": {
    "USDAED": 3.672985,
    "USDAFN": 68.232749,
    "USDALL": 83.558715,
    "USDAMD": 383.502854,
    "USDANG": 1.789699,
    "USDAOA": 917.00015,
    "USDARS": 1325.272673,
    "USDAUD": 1.534295,
    "USDAWG": 1.8025,
    "USDAZN": 1.6975,
    "USDBAM": 1.678726,
    "USDBBD": 2.017189,
    "USDBDT": 121.342432,
    "USDBGN": 1.677841,
    "USDBHD": 0.377014,
    "USDBIF": 2978.990118,
    "USDBMD": 1,
    "USDBND": 1.283861,
    "USDBOB": 6.900991,
    "USDBRL": 5.431197,
    "USDBSD": 0.999064,
    "USDBTC": 8.203109e-6,
    "USDBTN": 87.452899,
    "USDBWP": 13.442146,
    "USDBYN": 3.297455,
    "USDBYR": 19600,
    "USDBZD": 2.0068,
    "USDCAD": 1.37663,
    "USDCDF": 2889.999409,
    "USDCHF": 0.807198,
    "USDCLF": 0.024681,
    "USDCLP": 968.209662,
    "USDCNY": 7.181498,
    "USDCNH": 7.18632,
    "USDCOP": 4050.86,
    "USDCRC": 506.224779,
    "USDCUC": 1,
    "USDCUP": 26.5,
    "USDCVE": 94.644007,
    "USDCZK": 20.956033,
    "USDDJF": 177.901416,
    "USDDKK": 6.40227,
    "USDDOP": 61.011419,
    "USDDZD": 129.902425,
    "USDEGP": 48.429098,
    "USDERN": 15,
    "USDETB": 138.627715,
    "USDEUR": 0.85776,
    "USDFJD": 2.254898,
    "USDFKP": 0.743585,
    "USDGBP": 0.74297,
    "USDGEL": 2.701691,
    "USDGGP": 0.743585,
    "USDGHS": 10.536887,
    "USDGIP": 0.743585,
    "USDGMD": 72.473275,
    "USDGNF": 8663.249448,
    "USDGTQ": 7.66319,
    "USDGYD": 208.952405,
    "USDHKD": 7.849925,
    "USDHNL": 26.159526,
    "USDHRK": 6.461703,
    "USDHTG": 130.72148,
    "USDHUF": 338.792497,
    "USDIDR": 16266.8,
    "USDILS": 3.41363,
    "USDIMP": 0.743585,
    "USDINR": 87.616203,
    "USDIQD": 1308.355865,
    "USDIRR": 42124.999512,
    "USDISK": 122.630219,
    "USDJEP": 0.743585,
    "USDJMD": 159.95604,
    "USDJOD": 0.708995,
    "USDJPY": 147.562504,
    "USDKES": 129.202654,
    "USDKGS": 87.450101,
    "USDKHR": 4001.940439,
    "USDKMF": 422.150219,
    "USDKPW": 900.000119,
    "USDKRW": 1389.269868,
    "USDKWD": 0.30553,
    "USDKYD": 0.832325,
    "USDKZT": 539.727909,
    "USDLAK": 21608.514656,
    "USDLBP": 89486.545642,
    "USDLKR": 300.373375,
    "USDLRD": 200.248916,
    "USDLSL": 17.702931,
    "USDLTL": 2.95274,
    "USDLVL": 0.604889,
    "USDLYD": 5.416892,
    "USDMAD": 9.044505,
    "USDMDL": 16.768379,
    "USDMGA": 4408.879578,
    "USDMKD": 52.719056,
    "USDMMK": 2099.278286,
    "USDMNT": 3593.667467,
    "USDMOP": 8.075018,
    "USDMRU": 39.850605,
    "USDMUR": 45.38004,
    "USDMVR": 15.403747,
    "USDMWK": 1732.384873,
    "USDMXN": 18.582685,
    "USDMYR": 4.234027,
    "USDMZN": 63.959659,
    "USDNAD": 17.702931,
    "USDNGN": 1531.680479,
    "USDNIO": 36.765148,
    "USDNOK": 10.27799,
    "USDNPR": 139.966515,
    "USDNZD": 1.682978,
    "USDOMR": 0.384507,
    "USDPAB": 0.998755,
    "USDPEN": 3.535041,
    "USDPGK": 4.213997,
    "USDPHP": 57.003045,
    "USDPKR": 283.47835,
    "USDPLN": 3.644066,
    "USDPYG": 7482.677794,
    "USDQAR": 3.650401,
    "USDRON": 4.348968,
    "USDRSD": 100.467974,
    "USDRUB": 79.875385,
    "USDRWF": 1445.099361,
    "USDSAR": 3.754749,
    "USDSBD": 8.217066,
    "USDSCR": 14.741998,
    "USDSDG": 600.505228,
    "USDSEK": 9.56741,
    "USDSGD": 1.284025,
    "USDSHP": 0.785843,
    "USDSLE": 23.098543,
    "USDSLL": 20969.503947,
    "USDSOS": 570.964931,
    "USDSRD": 37.279032,
    "USDSTD": 20697.981008,
    "USDSTN": 21.03564,
    "USDSVC": 8.738681,
    "USDSYP": 13001.771596,
    "USDSZL": 17.701706,
    "USDTHB": 32.346502,
    "USDTJS": 9.328183,
    "USDTMT": 3.51,
    "USDTND": 2.928973,
    "USDTOP": 2.342103,
    "USDTRY": 40.71665,
    "USDTTD": 6.779108,
    "USDTWD": 29.927496,
    "USDTZS": 2475.00017,
    "USDUAH": 41.327043,
    "USDUGX": 3563.795545,
    "USDUYU": 40.075533,
    "USDUZS": 12578.000944,
    "USDVES": 128.74775,
    "USDVND": 26226.5,
    "USDVUV": 119.401149,
    "USDWST": 2.653917,
    "USDXAF": 563.200666,
    "USDXAG": 0.026317,
    "USDXAU": 0.000297,
    "USDXCD": 2.70255,
    "USDXCG": 1.800009,
    "USDXDR": 0.700441,
    "USDXOF": 563.203084,
    "USDXPF": 102.364705,
    "USDYER": 240.449827,
    "USDZAR": 17.73076,
    "USDZMK": 9001.196527,
    "USDZMW": 23.152942,
    "USDZWL": 321.999592
  },
  "createdAt": "2025-08-01T09:48:39.420000",
  "updatedAt": "2025-08-11T07:24:45.045000",
  "__v": 0
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## filters

**Document Count:** 5
**Sample Size:** 5

### Fields

| Field                     | Type          | Example                 |
| ------------------------- | ------------- | ----------------------- | ------------- | ------------- | --- |
| `_id`                     | ObjectId      |                         |
| `filters`                 | array<object> |                         |
| `filters[].key`           | string        | countries               |
| `filters[].title`         | string        | Supplier Country/Region |
| `filters[].type`          | string        | common                  |
| `filters[].value`         | array<object> | array (empty)           | array<object> | array<object> |     |
| `filters[].value[].id`    | integer       | 1                       |
| `filters[].value[].title` | string        | India                   |
| `filters[].value[].value` | string        | IN                      |
| `mappedId`                | string        | 003                     |
| `type`                    | string        | Products                |

### First Document (sanitized)

```json
{
  "_id": "684ae4bc86f966cd52545bd1",
  "type": "RFQ",
  "filters": [
    {
      "key": "category",
      "title": "Select Category",
      "type": "category",
      "value": []
    },
    {
      "key": "countries",
      "title": "Supplier Country/Region",
      "type": "common",
      "value": [
        {
          "id": 1,
          "value": "IN",
          "title": "India"
        },
        {
          "id": 2,
          "value": "CN",
          "title": "China"
        },
        {
          "id": 3,
          "value": "LK",
          "title": "Sri Lanka"
        },
        {
          "id": 4,
          "value": "US",
          "title": "United States"
        }
      ]
    },
    {
      "key": "featureSupplier",
      "title": "Supplier Features",
      "type": "common",
      "value": [
        {
          "id": 1,
          "value": "trueVerified",
          "title": "TrueVerified"
        },
        {
          "id": 2,
          "value": "trueAuthentic",
          "title": "TrueAuthentic"
        }
      ]
    }
  ],
  "mappedId": "006"
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## leads

**Document Count:** 233
**Sample Size:** 100

### Fields

| Field                         | Type            | Example       |
| ----------------------------- | --------------- | ------------- | --- |
| `__v`                         | integer         | 0             |
| `_id`                         | ObjectId        |               |
| `createdAt`                   | date            |               |
| `createdBy`                   | ObjectId        |               |
| `customerId`                  | ObjectId        |               |
| `interestProductIds`          | array<ObjectId> | array (empty) |     |
| `isArchived`                  | boolean         | False         |
| `isDraft`                     | boolean         | True          |
| `lastContact`                 | date            |               |
| `logs`                        | array (empty)   |               |
| `permission`                  | string          | Allowed       |
| `pricing`                     | object          |               |
| `pricing.bulkPrices`          | array<object>   |               |
| `pricing.bulkPrices[].maxQty` | integer         | 500           |
| `pricing.bulkPrices[].minQty` | integer         | 100           |
| `pricing.bulkPrices[].price`  | integer         | 1000          |
| `pricing.maxPrice`            | integer         | 70            |
| `pricing.minPrice`            | integer         | 50            |
| `pricing.pricingType`         | string          | bulk          |
| `pricing.unit`                | string          | pieces        |
| `pricing.unitPrice`           | integer         | 50            |
| `requirementDetails`          | string          |               |
| `source`                      | string          | Social Media  |
| `stage`                       | string          | New Inquiry   |
| `status`                      | string          | Not Connected |
| `threadId`                    | array (empty)   | array<string> |     |
| `updatedAt`                   | date            |               |
| `user_id`                     | ObjectId        |               |

### First Document (sanitized)

```json
{
  "_id": "685ccf12c3c7b30631b01117",
  "createdBy": "685b85aa523555fdc050e413",
  "customerId": "685ccf12c3c7b30631b01115",
  "interestProductIds": [],
  "requirementDetails": "",
  "stage": "New Inquiry",
  "source": "Offline",
  "status": "Not Connected",
  "permission": "Allowed",
  "logs": [],
  "isDraft": true,
  "isArchived": false,
  "threadId": [
    "6878c71a3fd4cfa568e80e1f",
    "6878c7393fd4cfa568e80e27",
    "6878c8523fd4cfa568e80e2f"
  ],
  "lastContact": "2025-06-26T04:39:46.257000",
  "createdAt": "2025-06-26T04:39:46.257000",
  "updatedAt": "2025-07-17T09:54:26.668000",
  "__v": 3
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## liveproducts

**Document Count:** 183
**Sample Size:** 100

### Fields

| Field                                               | Type          | Example                                           |
| --------------------------------------------------- | ------------- | ------------------------------------------------- | ------------- | ------------- | ------------- | ------------- | ------------- | --- |
| `__v`                                               | integer       | 0                                                 |
| `_id`                                               | ObjectId      |                                                   |
| `activeOffer`                                       | object        |                                                   |
| `activeOffer.expires`                               | date          | null                                              |               |
| `activeOffer.isApproved`                            | boolean       | False                                             |
| `activeOffer.offerId`                               | ObjectId      |                                                   |
| `activeOffer.offerInfo`                             | null          | object                                            |               |
| `activeOffer.offerInfo.buyQty`                      | integer       | 5                                                 |
| `activeOffer.offerInfo.currency`                    | object        |                                                   |
| `activeOffer.offerInfo.currency.code`               | string        | INR                                               |
| `activeOffer.offerInfo.currency.name`               | string        | Indian Rupee                                      |
| `activeOffer.offerInfo.currency.symbol`             | string        | ₹                                                 |
| `activeOffer.offerInfo.discountPercent`             | integer       | 5                                                 |
| `activeOffer.offerInfo.freeQty`                     | integer       | 1                                                 |
| `activeOffer.offerInfo.maxQty`                      | integer       | 100                                               |
| `activeOffer.offerInfo.minOrderQuantity`            | integer       | 800                                               |
| `activeOffer.offerInfo.minQty`                      | integer       | 50                                                |
| `activeOffer.offerInfo.offerType`                   | string        | limitedTime                                       |
| `activeOffer.offerInfo.pricing`                     | object        |                                                   |
| `activeOffer.offerInfo.pricing.bulkPrices`          | array<object> |                                                   |
| `activeOffer.offerInfo.pricing.bulkPrices[].maxQty` | integer       | 100                                               |
| `activeOffer.offerInfo.pricing.bulkPrices[].minQty` | integer       | 1                                                 |
| `activeOffer.offerInfo.pricing.bulkPrices[].price`  | integer       | number                                            | integer       | 1128          |
| `activeOffer.offerInfo.pricing.maxPrice`            | integer       | 475                                               |
| `activeOffer.offerInfo.pricing.minPrice`            | integer       | 95                                                |
| `activeOffer.offerInfo.pricing.pricingType`         | string        | negotiable                                        |
| `activeOffer.offerInfo.pricing.unit`                | string        | boxes                                             |
| `activeOffer.offerInfo.pricing.unitPrice`           | number        | integer                                           | 60000         |
| `activeOffer.offerInfo.unit`                        | string        | boxes                                             |
| `activeOffer.validOffer`                            | boolean       | False                                             |
| `analytics`                                         | object        |                                                   |
| `analytics.clicks`                                  | integer       | 0                                                 |
| `analytics.likes`                                   | integer       | 0                                                 |
| `analytics.shares`                                  | integer       | 1                                                 |
| `analytics.views`                                   | integer       | 30                                                |
| `attributes`                                        | array<object> | array (empty)                                     |               |
| `attributes[].isSuggested`                          | boolean       | False                                             |
| `attributes[].isValid`                              | integer       | 2                                                 |
| `attributes[].key`                                  | string        | Color                                             |
| `attributes[].values`                               | array<object> | array (empty)                                     |               |
| `attributes[].values[].isRemoved`                   | boolean       | False                                             |
| `attributes[].values[].isSelected`                  | boolean       | True                                              |
| `attributes[].values[].name`                        | string        | Red                                               |
| `brandName`                                         | string        | Ijoo                                              |
| `category`                                          | object        |                                                   |
| `category._id`                                      | string        | 67f514f976706f860309ebeb                          |
| `category.name`                                     | string        | Fashion                                           |
| `category.uniqueId`                                 | string        | CA6c3cab3c96                                      |
| `categorySuggestion`                                | object        |                                                   |
| `categorySuggestion.industry`                       | string        | business-services                                 |
| `categorySuggestion.reason`                         | string        | I cannot find the category.                       |
| `categorySuggestion.suggestedCategory`              | string        | Toys                                              |
| `certificates`                                      | array<object> |                                                   |
| `certificates[].alt`                                | string        | dummy                                             |
| `certificates[].exten`                              | string        | pdf                                               |
| `certificates[].name`                               | string        | Demo                                              |
| `certificates[].size`                               | integer       | 13264                                             |
| `certificates[].src`                                | string        | assets/wZvN4JPHvRlVmAXSglQ_N.pdf                  |
| `countryOfOrigin`                                   | object        |                                                   |
| `countryOfOrigin.code`                              | string        | AX                                                |
| `countryOfOrigin.name`                              | string        | Aland Islands                                     |
| `createdAt`                                         | date          |                                                   |
| `createdBy`                                         | ObjectId      |                                                   |
| `currency`                                          | string        | object                                            | USD           |
| `currency.code`                                     | string        | INR                                               |
| `currency.name`                                     | string        | Indian Rupee                                      |
| `currency.symbol`                                   | string        | ₹                                                 |
| `customization`                                     | array<string> |                                                   |
| `detailedDescription`                               | string        | sarfwr                                            |
| `dispatchLeadTime`                                  | object        |                                                   |
| `dispatchLeadTime.max_day`                          | integer       | 2                                                 |
| `dispatchLeadTime.min_day`                          | integer       | 2                                                 |
| `faqs`                                              | array<object> |                                                   |
| `faqs[].answer`                                     | string        | It takes 5-7 business days for standard shipping. |
| `faqs[].question`                                   | string        | Does the laptop come with a warranty?             |
| `globalRatings`                                     | object        |                                                   |
| `globalRatings.averageRating`                       | integer       | 4                                                 |
| `globalRatings.totalRatings`                        | integer       | 2                                                 |
| `incoTerms`                                         | string        | FOB                                               |
| `internationalShipping`                             | string        | no                                                |
| `isCustomizable`                                    | boolean       | False                                             |
| `liveUrl`                                           | string        | Shoe_BPeb59239566                                 |
| `minOrderQuantity`                                  | integer       | 55                                                |
| `moqUnit`                                           | string        | pieces                                            |
| `otherPaymentMethod`                                | string        | UPI                                               |
| `paymentMethods`                                    | array<string> |                                                   |
| `paymentTerms`                                      | string        | ADVANCE_50_DISPATCH_50                            |
| `portOfDispatch`                                    | string        | Thoothukudi                                       |
| `pricing`                                           | object        |                                                   |
| `pricing.bulkPrices`                                | array<object> |                                                   |
| `pricing.bulkPrices[].maxQty`                       | integer       | 40                                                |
| `pricing.bulkPrices[].minQty`                       | integer       | 5                                                 |
| `pricing.bulkPrices[].price`                        | integer       | 30                                                |
| `pricing.maxPrice`                                  | integer       | 1000                                              |
| `pricing.minPrice`                                  | integer       | 500                                               |
| `pricing.pricingType`                               | string        | fixed                                             |
| `pricing.unit`                                      | string        | boxes                                             |
| `pricing.unitPrice`                                 | integer       | 500                                               |
| `productApplications`                               | string        | erwertw4trw                                       |
| `productBrochure`                                   | object        |                                                   |
| `productBrochure.alt`                               | string        | dummy                                             |
| `productBrochure.exten`                             | string        | pdf                                               |
| `productBrochure.size`                              | integer       | 13264                                             |
| `productBrochure.src`                               | string        | https://example.com/images/eco-bottle-blue.jpg    |
| `productCategory`                                   | object        |                                                   |
| `productCategory._id`                               | string        | 67f5124876706f860309ebd7                          |
| `productCategory.name`                              | string        | Watches                                           |
| `productDescription`                                | string        | jsdfgeiygfefgeiufgegfewbfe                        |
| `productGroup`                                      | ObjectId      |                                                   |
| `productImage`                                      | array<object> |                                                   |
| `productImage[].alt`                                | string        | andres-jasso-PqbL_mxmaUE-unsplash                 |
| `productImage[].exten`                              | string        | png                                               |
| `productImage[].size`                               | integer       | 137885                                            |
| `productImage[].src`                                | string        | assets/Cz8F5rnA7fllX46iiEct\_.jpg                 |
| `productKeyword`                                    | array (empty) | array<string>                                     |               |
| `productName`                                       | string        | Shoe                                              |
| `productVideo`                                      | string        | object                                            | pathto video  |
| `productVideo.alt`                                  | string        |                                                   |
| `productVideo.exten`                                | string        | mp4                                               |
| `productVideo.size`                                 | integer       | 3485909                                           |
| `productVideo.src`                                  | string        |                                                   |
| `productionCapacity`                                | object        |                                                   |
| `productionCapacity.duration`                       | string        | weekly                                            |
| `productionCapacity.quantity`                       | integer       | 23                                                |
| `productionCapacity.unit`                           | string        | pieces                                            |
| `productionLeadTime`                                | object        |                                                   |
| `productionLeadTime.max_day`                        | integer       | 14                                                |
| `productionLeadTime.max_quantity`                   | integer       | 0                                                 |
| `productionLeadTime.min_day`                        | integer       | 8                                                 |
| `productionLeadTime.min_quantity`                   | integer       | 0                                                 |
| `productionLeadTime.unit`                           | string        | unit                                              |
| `salesProductId`                                    | ObjectId      |                                                   |
| `samplesAvailability`                               | object        |                                                   |
| `samplesAvailability.availabilityType`              | string        | free                                              |
| `samplesAvailability.sampleLeadTime`                | object        |                                                   |
| `samplesAvailability.sampleLeadTime._id`            | string        | 1-rr                                              |
| `samplesAvailability.sampleLeadTime.max_day`        | integer       | 7                                                 |
| `samplesAvailability.sampleLeadTime.min_day`        | integer       | 4                                                 |
| `samplesAvailability.sampleLeadTime.name`           | string        | 1-2 days                                          |
| `samplesAvailability.samplePrice`                   | integer       | 10                                                |
| `samplesAvailability.sampleUnit`                    | string        | box                                               |
| `shipmentIdentifier`                                | string        | 1212515                                           |
| `shippingMethod`                                    | array<string> |                                                   |
| `shippingQty`                                       | integer       | 65                                                |
| `shippingUnit`                                      | string        | Carton                                            |
| `showcase`                                          | boolean       | False                                             |
| `skuCode`                                           | string        | SKU\_\_0967                                       |
| `status`                                            | string        | live                                              |
| `stockAvailability`                                 | string        | inStock                                           |
| `subCategory`                                       | object        |                                                   |
| `subCategory._id`                                   | string        | 67f515a976706f860309ebf5                          |
| `subCategory.name`                                  | string        | sports                                            |
| `subCategory.uniqueId`                              | string        | SC6e16b67695                                      |
| `uniqueId`                                          | string        | BPeb59239566                                      |
| `updatedAt`                                         | date          |                                                   |
| `variantAttributes`                                 | array<object> | array (empty)                                     |               |
| `variantAttributes[].key`                           | string        | Color                                             |
| `variantAttributes[].values`                        | array<string> |                                                   |
| `variants`                                          | array<object> | array (empty)                                     |               |
| `variants[]._id`                                    | ObjectId      |                                                   |
| `variants[].attributes`                             | object        |                                                   |
| `variants[].attributes.Brand`                       | string        | Samsung                                           |
| `variants[].attributes.Cocoa Content`               | string        | 70% Dark                                          |
| `variants[].attributes.Color`                       | string        | Red                                               |
| `variants[].attributes.Color Options`               | string        | Black                                             |
| `variants[].attributes.Colour`                      | string        | Red                                               |
| `variants[].attributes.Expect`                      | string        | new                                               |
| `variants[].attributes.Flavor`                      | string        | Chocolate Chip                                    |
| `variants[].attributes.Gender Suitability`          | string        | Unisex                                            |
| `variants[].attributes.Heel Size`                   | string        | 5cm                                               |
| `variants[].attributes.Material`                    | string        | Cotton                                            |
| `variants[].attributes.Material Type`               | string        | Suede                                             |
| `variants[].attributes.OS`                          | string        | Andriod                                           |
| `variants[].attributes.Screen Size`                 | string        | 13 inch                                           |
| `variants[].attributes.Screen Size Range`           | string        | 5 to 6 inches                                     |
| `variants[].attributes.Size`                        | string        | 7                                                 |
| `variants[].attributes.Style`                       | string        | Casual                                            |
| `variants[].attributes.Type`                        | string        | Mangoose                                          |
| `variants[].attributes.color`                       | string        | red                                               |
| `variants[].attributes.colour`                      | string        | white + black                                     |
| `variants[].attributes.gun`                         | string        | air gun                                           |
| `variants[].attributes.size`                        | string        | lare                                              |
| `variants[].attributes.types`                       | string        | type 1                                            |
| `variants[].available`                              | boolean       | True                                              |
| `variants[].isActive`                               | boolean       | True                                              |
| `variants[].isDeleted`                              | boolean       | False                                             |
| `variants[].minOrderQuantity`                       | integer       | 23                                                |
| `variants[].moqUnit`                                | string        | pieces                                            |
| `variants[].pricing`                                | object        |                                                   |
| `variants[].pricing.bulkPrices`                     | array<object> |                                                   |
| `variants[].pricing.bulkPrices[].maxQty`            | integer       | 70                                                |
| `variants[].pricing.bulkPrices[].minQty`            | integer       | 40                                                |
| `variants[].pricing.bulkPrices[].price`             | integer       | 2000                                              |
| `variants[].pricing.maxPrice`                       | integer       | 700                                               |
| `variants[].pricing.minPrice`                       | integer       | 500                                               |
| `variants[].pricing.pricingType`                    | string        | fixed                                             |
| `variants[].pricing.unit`                           | string        | boxes                                             |
| `variants[].pricing.unitPrice`                      | integer       | 500                                               |
| `variants[].skuCode`                                | string        | SKU_09                                            |
| `variants[].variantImg`                             | array<object> | array (empty)                                     | array (empty) | array<object> | array (empty) | array<object> | array (empty) |     |
| `variants[].variantImg[].alt`                       | string        | assets/vA-dZ63C4gk71FewoTybr.jpg                  |
| `variants[].variantImg[].exten`                     | string        | image/jpeg                                        |
| `variants[].variantImg[].size`                      | integer       | 46505                                             |
| `variants[].variantImg[].src`                       | string        | assets/vA-dZ63C4gk71FewoTybr.jpg                  |
| `variants[].variantName`                            | string        | Red / 7                                           |
| `youtubeUrl`                                        | string        |                                                   |

### First Document (sanitized)

```json
{
  "_id": "685007b967aabc8a4d7c0857",
  "productName": "new id map",
  "createdBy": "685b89a6a8f68cc8e3c20069",
  "productDescription": "testset",
  "category": {
    "_id": "67f514ee76706f860309ebe9",
    "name": "Electronics",
    "uniqueId": "CAee40f0e5be"
  },
  "subCategory": {
    "_id": "67f5158976706f860309ebf3",
    "name": "Laptops",
    "uniqueId": "SC767f777539"
  },
  "productCategory": {
    "_id": "67f5124876706f860309ebd1",
    "name": "Gaming Laptops"
  },
  "productImage": [
    {
      "src": "assets/download (3)_40565315-c872-4213-acff-f6055810ba1d_1750075068321.jpg",
      "alt": "download (3)",
      "exten": "jpg",
      "size": 6217
    }
  ],
  "currency": {
    "code": "INR",
    "name": "Indian Rupee",
    "symbol": "₹"
  },
  "pricing": {
    "pricingType": "fixed",
    "unitPrice": 34
  },
  "minOrderQuantity": 34,
  "moqUnit": "pieces",
  "brandName": "Chocolate Lava",
  "showcase": false,
  "status": "live",
  "activeOffer": {
    "offerId": "685006e4c7bfad0104f348d3",
    "validOffer": false
  },
  "salesProductId": "685006e2c7bfad0104f348d0",
  "uniqueId": "BP000a6a108a",
  "liveUrl": "new_id_map_BP000a6a108a",
  "createdAt": "2025-06-16T11:58:26.837000",
  "updatedAt": "2025-07-21T07:14:27.706000",
  "__v": 0,
  "globalRatings": {
    "averageRating": 4.35,
    "totalRatings": 20
  },
  "analytics": {
    "views": 56
  }
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

**productName_text**

- Keys:
  - `_fts`: text
  - `_ftsx`: ascending

---

## marketcatalogs

**Document Count:** 1
**Sample Size:** 1

### Fields

| Field              | Type          | Example                  |
| ------------------ | ------------- | ------------------------ |
| `__v`              | integer       | 0                        |
| `_id`              | ObjectId      |                          |
| `analytics`        | object        |                          |
| `analytics.shares` | integer       | 0                        |
| `analytics.views`  | integer       | 0                        |
| `businessType`     | string        | unregistered             |
| `catalogName`      | string        | Techverse Catalog        |
| `createdAt`        | date          |                          |
| `industry`         | array<string> |                          |
| `legalName`        | string        | Techverse Innovations    |
| `legalStatus`      | string        | sole_proprietorship      |
| `productIds`       | array (empty) |                          |
| `status`           | string        | pending                  |
| `subDomain`        | string        | techverse-innovations    |
| `updatedAt`        | date          |                          |
| `userId`           | string        | 685b8a51a8f68cc8e3c2008a |

### First Document (sanitized)

```json
{
  "_id": "688ff6fb1883b50be5f1d4ff",
  "catalogName": "Techverse Catalog",
  "subDomain": "techverse-innovations",
  "userId": "685b8a51a8f68cc8e3c2008a",
  "legalName": "Techverse Innovations",
  "businessType": "unregistered",
  "legalStatus": "sole_proprietorship",
  "industry": ["technology, software"],
  "status": "pending",
  "productIds": [],
  "analytics": {
    "views": 0,
    "shares": 0
  },
  "createdAt": "2025-08-03T23:55:39.542000",
  "updatedAt": "2025-08-03T23:55:39.542000",
  "__v": 0
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

**subDomain_1**

- Type: Unique
- Keys:
  - `subDomain`: ascending

---

## messages

**Document Count:** 137
**Sample Size:** 100

### Fields

| Field               | Type          | Example                        |
| ------------------- | ------------- | ------------------------------ | --- |
| `__v`               | integer       | 0                              |
| `_id`               | ObjectId      |                                |
| `attachment`        | array<object> | array (empty)                  |     |
| `attachment[].alt`  | string        | image1.jpg                     |
| `attachment[].extn` | string        | jpg                            |
| `attachment[].size` | integer       | 4                              |
| `attachment[].src`  | string        | https://example.com/image1.jpg |
| `bcc`               | array (empty) | array<string>                  |     |
| `cc`                | array (empty) | array<string>                  |     |
| `content`           | string        | product 123                    |
| `createdAt`         | date          |                                |
| `createdBy`         | ObjectId      |                                |
| `fav`               | boolean       | False                          |
| `isArchive`         | boolean       | False                          |
| `isDeleted`         | boolean       | False                          |
| `pageType`          | string        | connect                        |
| `reactions`         | array (empty) |                                |
| `read`              | boolean       | False                          |
| `subject`           | string        | Request                        |
| `threadId`          | string        | 686658e3fecc2b65af6f3187       |
| `to`                | array (empty) | array<string>                  |     |
| `type`              | string        | chat                           |
| `updatedAt`         | date          |                                |
| `user_id`           | ObjectId      |                                |

### First Document (sanitized)

```json
{
  "_id": "685e96de18dffec597f7e058",
  "createdBy": "685b80efeb6995d34ef05bed",
  "subject": "New Product Inquiry 9",
  "content": "I'm interested in this product. Can you provide more details?",
  "attachment": [
    {
      "src": "https://example.com/image1.jpg",
      "alt": "image1.jpg",
      "extn": "jpg",
      "size": 4
    }
  ],
  "fav": false,
  "read": false,
  "threadId": "685e96de18dffec597f7e057",
  "isDeleted": false,
  "isArchive": false,
  "to": [],
  "type": "chat",
  "cc": [],
  "bcc": [],
  "createdAt": "2025-06-27T13:04:30.447000",
  "updatedAt": "2025-06-27T13:04:30.447000",
  "__v": 0
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## otps

**Document Count:** 2,291
**Sample Size:** 100

### Fields

| Field         | Type     | Example                  |
| ------------- | -------- | ------------------------ |
| `__v`         | integer  | 0                        |
| `_id`         | ObjectId |                          |
| `countryCode` | string   | +91                      |
| `createdAt`   | date     |                          |
| `email`       | string   | antoraphael100@gmail.com |
| `expiry_date` | date     |                          |
| `otp`         | string   | 571393                   |
| `phoneNo`     | string   | 9894722519               |
| `retryCount`  | integer  | 0                        |
| `updatedAt`   | date     |                          |
| `verified`    | boolean  | True                     |

### First Document (sanitized)

```json
{
  "_id": "685b80528fb2bc1c77d7c511",
  "email": "umapreethi.s@solutionchamps.com",
  "otp": "[REDACTED]",
  "expiry_date": "2025-06-25T05:06:30.839000",
  "verified": true,
  "retryCount": 0,
  "createdAt": "2025-06-25T04:51:30.876000",
  "updatedAt": "2025-08-08T16:45:14.573000",
  "__v": 0
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## payments

**Document Count:** 2
**Sample Size:** 2

### Fields

| Field                         | Type     | Example            |
| ----------------------------- | -------- | ------------------ |
| `_id`                         | ObjectId |                    |
| `createdBy`                   | ObjectId |                    |
| `invoice`                     | string   | INV-2025-0001      |
| `paymentDate`                 | date     |                    |
| `paymentMethod`               | object   |                    |
| `paymentMethod.method`        | string   | card               |
| `paymentMethod.number`        | string   | 4111111111111111   |
| `paymentResult`               | object   |                    |
| `paymentResult.statusMessage` | string   | Payment successful |
| `paymentResult.transactionId` | string   | txn_1234567890     |
| `paymentStatus`               | string   | paid               |
| `totalAmount`                 | string   | 999.00             |

### First Document (sanitized)

```json
{
  "_id": "6895f7a16e675d454fa8761b",
  "createdBy": "685b83c9640c0efe0929cfa6",
  "paymentDate": "2025-08-08T00:00:00",
  "paymentMethod": {
    "method": "card",
    "number": "4111111111111111"
  },
  "paymentStatus": "paid",
  "invoice": "INV-2025-0001",
  "totalAmount": "999.00",
  "paymentResult": {
    "transactionId": "txn_1234567890",
    "statusMessage": "Payment successful"
  }
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## productcategories

**Document Count:** 33
**Sample Size:** 33

### Fields

| Field      | Type     | Example                  |
| ---------- | -------- | ------------------------ |
| `_id`      | ObjectId |                          |
| `name`     | string   | Strategy Games           |
| `parentId` | string   | 6620c91a1f1c8a9a1b1c1010 |
| `uniqueId` | string   | PRD-019                  |

### First Document (sanitized)

```json
{
  "_id": "67f5124876706f860309ebcf",
  "uniqueId": "PRD-001",
  "name": "Smartphones",
  "parentId": "67f5154376706f860309ebf0"
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

**uniqueId_1**

- Type: Unique
- Keys:
  - `uniqueId`: ascending

---

## quotations

**Document Count:** 0
**Sample Size:** 0

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## remarks

**Document Count:** 124
**Sample Size:** 100

### Fields

| Field                 | Type          | Example          |
| --------------------- | ------------- | ---------------- |
| `__v`                 | integer       | 0                |
| `_id`                 | ObjectId      |                  |
| `createdAt`           | date          |                  |
| `remarks`             | array<object> |                  |
| `remarks[]._id`       | ObjectId      |                  |
| `remarks[].createdAt` | date          |                  |
| `remarks[].reason`    | string        | Wrong color/size |
| `remarks[].remark`    | string        | d                |
| `remarks[].to`        | string        | test             |
| `remarks[].updatedAt` | date          |                  |
| `type`                | string        | offer            |
| `typeId`              | ObjectId      |                  |
| `updatedAt`           | date          |                  |

### First Document (sanitized)

```json
{
  "_id": "686f86860ce34c9c033bb3b1",
  "typeId": "6826ce429ad870fb6764cefc",
  "type": "product",
  "remarks": [
    {
      "to": "admin",
      "reason": "Product details are incorrect",
      "remark": "Please review the pricing section and submit again.",
      "_id": "686f86860ce34c9c033bb3b2",
      "createdAt": "2025-07-10T09:23:18.876000",
      "updatedAt": "2025-07-10T09:23:18.876000"
    },
    {
      "to": "admin",
      "reason": "Product details are incorrect",
      "remark": "Please review the pricing section and submit again.",
      "_id": "686f873d0ce34c9c033bb3bc",
      "createdAt": "2025-07-10T09:26:21.983000",
      "updatedAt": "2025-07-10T09:26:21.983000"
    }
  ],
  "createdAt": "2025-07-10T09:23:18.877000",
  "updatedAt": "2025-07-10T09:26:21.984000",
  "__v": 1
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## reviews

**Document Count:** 0
**Sample Size:** 0

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## rfqcarts

**Document Count:** 40
**Sample Size:** 40

### Fields

| Field                                     | Type          | Example                            |
| ----------------------------------------- | ------------- | ---------------------------------- | ------------- | --- |
| `__v`                                     | integer       | 0                                  |
| `_id`                                     | ObjectId      |                                    |
| `createdAt`                               | date          |                                    |
| `createdBy`                               | ObjectId      |                                    |
| `isActive`                                | boolean       | True                               |
| `productId`                               | ObjectId      |                                    |
| `selectedVariants`                        | array<object> |                                    |
| `selectedVariants[]._id`                  | string        | 6870b86496c7dd13bd60101a           |
| `selectedVariants[].quantity`             | integer       | 50                                 |
| `totalOrderQuantity`                      | integer       | 50                                 |
| `updatedAt`                               | date          |                                    |
| `variants`                                | array<object> |                                    |
| `variants[]._id`                          | ObjectId      |                                    |
| `variants[].attributes`                   | object        |                                    |
| `variants[].attributes.Brand`             | string        | Samsung                            |
| `variants[].attributes.Color`             | string        | red                                |
| `variants[].attributes.Color Options`     | string        | Black                              |
| `variants[].attributes.Material`          | string        | Cotton                             |
| `variants[].attributes.Screen Size`       | string        | 13 inch                            |
| `variants[].attributes.Screen Size Range` | string        | 5 to 6 inches                      |
| `variants[].attributes.Size`              | string        | 7                                  |
| `variants[].attributes.Size Options`      | string        | US 7                               |
| `variants[].attributes.Style`             | string        | Sneakers                           |
| `variants[].attributes.color`             | string        | red                                |
| `variants[].attributes.features `         | string        | 4g                                 |
| `variants[].available`                    | boolean       | True                               |
| `variants[].isActive`                     | boolean       | True                               |
| `variants[].isDeleted`                    | boolean       | False                              |
| `variants[].minOrderQuantity`             | integer       | 100                                |
| `variants[].moqUnit`                      | string        | pieces                             |
| `variants[].pricing`                      | object        |                                    |
| `variants[].pricing.bulkPrices`           | array<object> |                                    |
| `variants[].pricing.bulkPrices[].maxQty`  | integer       | 200                                |
| `variants[].pricing.bulkPrices[].minQty`  | integer       | 100                                |
| `variants[].pricing.bulkPrices[].price`   | integer       | 100                                |
| `variants[].pricing.maxPrice`             | integer       | 600                                |
| `variants[].pricing.minPrice`             | integer       | 500                                |
| `variants[].pricing.pricingType`          | string        | fixed                              |
| `variants[].pricing.unit`                 | string        | pieces                             |
| `variants[].pricing.unitPrice`            | integer       | 10                                 |
| `variants[].skuCode`                      | string        | sdo0011                            |
| `variants[].variantImg`                   | array<object> | array<object>                      | array (empty) |     |
| `variants[].variantImg[].alt`             | string        | Samsung-Mobile-Phone...\_imresizer |
| `variants[].variantImg[].exten`           | string        | jpg                                |
| `variants[].variantImg[].size`            | integer       | 58460                              |
| `variants[].variantImg[].src`             | string        | assets/P8o2kMDTuATV5zxuIScId.jpg   |
| `variants[].variantName`                  | string        | 4g                                 |

### First Document (sanitized)

```json
{
  "_id": "68660b7480092497302b509f",
  "createdBy": "685e3e9a909298eae0b63672",
  "productId": "68660aa1dcf99b3ed9be9c68",
  "variants": [
    {
      "variantName": "red / 7",
      "variantImg": [
        {
          "src": "assets/domino-studio-164_6wVEHfI-unsplash_49709745-3106-4cc1-bed3-f21d055ca5bd_1751517559491.png",
          "alt": "domino-studio-164_6wVEHfI-unsplash",
          "exten": "png",
          "size": 113846
        }
      ],
      "pricing": {
        "pricingType": "fixed",
        "unitPrice": 500
      },
      "attributes": {
        "Color": "red",
        "Size": "7"
      },
      "available": true,
      "skuCode": "hsfh=-0",
      "minOrderQuantity": 500,
      "moqUnit": "pieces",
      "isDeleted": false,
      "isActive": true,
      "_id": "686609c4dcf99b3ed9be9c4f"
    },
    {
      "variantName": "red / 8",
      "variantImg": [
        {
          "src": "assets/domino-studio-164_6wVEHfI-unsplash_cea1451a-e61a-4392-9103-28d0b480a26f_1751517617834.png",
          "alt": "domino-studio-164_6wVEHfI-unsplash",
          "exten": "png",
          "size": 113846
        }
      ],
      "pricing": {
        "pricingType": "fixed",
        "unitPrice": 500
      },
      "attributes": {
        "Color": "red",
        "Size": "8"
      },
      "available": true,
      "skuCode": "sefwe",
      "minOrderQuantity": 500,
      "moqUnit": "boxes",
      "isDeleted": false,
      "isActive": true,
      "_id": "686609c4dcf99b3ed9be9c50"
    }
  ],
  "selectedVariants": [
    {
      "_id": "686609c4dcf99b3ed9be9c4f",
      "quantity": 500
    },
    {
      "_id": "686609c4dcf99b3ed9be9c50",
      "quantity": 5
    }
  ],
  "isActive": false,
  "totalOrderQuantity": 505,
  "createdAt": "2025-07-03T04:47:48.954000",
  "updatedAt": "2025-07-03T05:06:17.849000",
  "__v": 0
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## roles

**Document Count:** 0
**Sample Size:** 0

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## salesproductgroups

**Document Count:** 39
**Sample Size:** 39

### Fields

| Field             | Type          | Example |
| ----------------- | ------------- | ------- |
| `__v`             | integer       | 0       |
| `_id`             | ObjectId      |         |
| `createdAt`       | date          |         |
| `groupName`       | string        | CHARGER |
| `mappedProductId` | array (empty) |         |
| `updatedAt`       | date          |         |

### First Document (sanitized)

```json
{
  "_id": "67e2a94849683c3e7f217256",
  "groupName": "group1",
  "createdAt": "2025-03-25T13:02:00.946000",
  "updatedAt": "2025-03-25T13:02:00.946000",
  "__v": 0
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## salesproductionleadtimes

**Document Count:** 2
**Sample Size:** 2

### Fields

| Field                  | Type          | Example |
| ---------------------- | ------------- | ------- |
| `__v`                  | integer       | 0       |
| `_id`                  | ObjectId      |         |
| `createdAt`            | date          |         |
| `createdBy`            | ObjectId      |         |
| `default`              | boolean       | False   |
| `updatedAt`            | date          |         |
| `value`                | array<object> |         |
| `value[].max_day`      | integer       | 3       |
| `value[].max_quantity` | integer       | 0       |
| `value[].min_day`      | integer       | 1       |
| `value[].min_quantity` | integer       | 0       |
| `value[].unit`         | string        | unit    |

### First Document (sanitized)

```json
{
  "_id": "680f2440c7c2516d4f0da919",
  "default": true,
  "value": [
    {
      "min_day": 1,
      "max_day": 3,
      "min_quantity": 0,
      "max_quantity": 0,
      "unit": "unit"
    },
    {
      "min_day": 4,
      "max_day": 7,
      "min_quantity": 0,
      "max_quantity": 0,
      "unit": "unit"
    },
    {
      "min_day": 8,
      "max_day": 14,
      "min_quantity": 0,
      "max_quantity": 0,
      "unit": "unit"
    },
    {
      "min_day": 15,
      "max_day": 13,
      "min_quantity": 0,
      "max_quantity": 0,
      "unit": "unit"
    },
    {
      "min_day": 15,
      "max_day": 30,
      "min_quantity": 0,
      "max_quantity": 0,
      "unit": "unit"
    }
  ]
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## salesproducts

**Document Count:** 513
**Sample Size:** 100

### Fields

| Field                                               | Type          | Example                                        |
| --------------------------------------------------- | ------------- | ---------------------------------------------- | ------------- | ------------- | ------------- | ------------- | ------------- | --- |
| `__v`                                               | integer       | 0                                              |
| `_id`                                               | ObjectId      |                                                |
| `activeOffer`                                       | object        |                                                |
| `activeOffer.expires`                               | date          |                                                |
| `activeOffer.isApproved`                            | boolean       | False                                          |
| `activeOffer.offerId`                               | ObjectId      |                                                |
| `activeOffer.offerInfo`                             | object        |                                                |
| `activeOffer.offerInfo.buyQty`                      | integer       | 50                                             |
| `activeOffer.offerInfo.currency`                    | string        | object                                         | INR           |
| `activeOffer.offerInfo.currency.code`               | string        | INR                                            |
| `activeOffer.offerInfo.currency.name`               | string        | Indian Rupee                                   |
| `activeOffer.offerInfo.currency.symbol`             | string        | ₹                                              |
| `activeOffer.offerInfo.discountPercent`             | integer       | 25                                             |
| `activeOffer.offerInfo.freeQty`                     | integer       | 50                                             |
| `activeOffer.offerInfo.maxQty`                      | integer       | 100                                            |
| `activeOffer.offerInfo.minOrderQuantity`            | integer       | 10                                             |
| `activeOffer.offerInfo.minQty`                      | integer       | 55                                             |
| `activeOffer.offerInfo.offerType`                   | string        | fixedDiscount                                  |
| `activeOffer.offerInfo.pricing`                     | object        |                                                |
| `activeOffer.offerInfo.pricing.bulkPrices`          | array<object> |                                                |
| `activeOffer.offerInfo.pricing.bulkPrices[].maxQty` | integer       | 98                                             |
| `activeOffer.offerInfo.pricing.bulkPrices[].minQty` | integer       | 85                                             |
| `activeOffer.offerInfo.pricing.bulkPrices[].price`  | number        | integer                                        | 57.75         |
| `activeOffer.offerInfo.pricing.pricingType`         | string        | fixed                                          |
| `activeOffer.offerInfo.pricing.unit`                | string        | boxes                                          |
| `activeOffer.offerInfo.pricing.unitPrice`           | number        | integer                                        | 75000         |
| `activeOffer.offerInfo.unit`                        | string        | pieces                                         |
| `activeOffer.validOffer`                            | boolean       | True                                           |
| `assignTo`                                          | ObjectId      |                                                |
| `attributes`                                        | array<object> | array (empty)                                  |               |
| `attributes[].isSuggested`                          | boolean       | False                                          |
| `attributes[].isValid`                              | integer       | 1                                              |
| `attributes[].key`                                  | string        | Brand                                          |
| `attributes[].values`                               | array<object> |                                                |
| `attributes[].values[].isRemoved`                   | boolean       | False                                          |
| `attributes[].values[].isSelected`                  | boolean       | True                                           |
| `attributes[].values[].name`                        | string        | Samsung                                        |
| `brandName`                                         | string        | tes brand                                      |
| `category`                                          | object        |                                                |
| `category._id`                                      | string        | 67f514ee76706f860309ebe9                       |
| `category.name`                                     | string        | Electronics                                    |
| `category.uniqueId`                                 | string        | CAee40f0e5be                                   |
| `categorySuggestion`                                | object        |                                                |
| `categorySuggestion.industry`                       | string        | business-services                              |
| `categorySuggestion.reason`                         | string        | I cannot find the category.                    |
| `categorySuggestion.suggestedCategory`              | string        | toys                                           |
| `certificates`                                      | array<object> |                                                |
| `certificates[].alt`                                | string        | Employer Survey (1)                            |
| `certificates[].exten`                              | string        | pdf                                            |
| `certificates[].name`                               | string        | iso                                            |
| `certificates[].size`                               | integer       | 684280                                         |
| `certificates[].src`                                | string        | assets/kJVs_JFoIG0Im_CAW4X2C.pdf               |
| `countryOfOrigin`                                   | object        |                                                |
| `countryOfOrigin.code`                              | string        | IN                                             |
| `countryOfOrigin.name`                              | string        | India                                          |
| `createdAt`                                         | date          |                                                |
| `createdBy`                                         | ObjectId      |                                                |
| `currency`                                          | string        | object                                         | USD           |
| `currency.code`                                     | string        | INR                                            |
| `currency.name`                                     | string        | Indian Rupee                                   |
| `currency.symbol`                                   | string        | ₹                                              |
| `customization`                                     | array<string> |                                                |
| `detailedDescription`                               | string        | Product Description                            |
| `dispatchLeadTime`                                  | object        |                                                |
| `dispatchLeadTime.max_day`                          | integer       | null                                           | 2             |
| `dispatchLeadTime.min_day`                          | integer       | null                                           | 2             |
| `faqs`                                              | array<object> |                                                |
| `faqs[].answer`                                     | string        |                                                |
| `faqs[].question`                                   | string        | Can I buy an insurance plan for my new iPhone? |
| `incoTerms`                                         | string        | CIF                                            |
| `internationalShipping`                             | string        | yes                                            |
| `isArchived`                                        | boolean       | False                                          |
| `isCustomizable`                                    | boolean       | True                                           |
| `isDraft`                                           | boolean       | False                                          |
| `isQuickInsert`                                     | boolean       | True                                           |
| `liveProductId`                                     | ObjectId      |                                                |
| `minOrderQuantity`                                  | integer       | 10                                             |
| `moqUnit`                                           | string        | pieces                                         |
| `otherPaymentMethod`                                | string        | UPI                                            |
| `paymentMethods`                                    | array<string> |                                                |
| `paymentTerms`                                      | string        | ADVANCE_50_DISPATCH_50                         |
| `portOfDispatch`                                    | string        | sea                                            |
| `pricing`                                           | object        |                                                |
| `pricing.bulkPrices`                                | array<object> |                                                |
| `pricing.bulkPrices[].maxQty`                       | integer       | 10                                             |
| `pricing.bulkPrices[].minQty`                       | integer       | 1                                              |
| `pricing.bulkPrices[].price`                        | integer       | 100                                            |
| `pricing.maxPrice`                                  | integer       | 2000                                           |
| `pricing.minPrice`                                  | integer       | 300                                            |
| `pricing.pricingType`                               | string        | bulk                                           |
| `pricing.unit`                                      | string        | pieces                                         |
| `pricing.unitPrice`                                 | integer       | 10000                                          |
| `productApplications`                               | string        | Applications                                   |
| `productBrochure`                                   | object        |                                                |
| `productBrochure.alt`                               | string        | Employer Survey                                |
| `productBrochure.exten`                             | string        | pdf                                            |
| `productBrochure.size`                              | integer       | 684280                                         |
| `productBrochure.src`                               | string        |                                                |
| `productCategory`                                   | object        |                                                |
| `productCategory._id`                               | string        | 67f5154376706f860309ebf0                       |
| `productCategory.name`                              | string        | Feature Phones                                 |
| `productDescription`                                | string        | some product description                       |
| `productGroup`                                      | ObjectId      |                                                |
| `productId`                                         | string        | PRD-f7696e40b7                                 |
| `productImage`                                      | array<object> |                                                |
| `productImage[].alt`                                | string        | sdfsdf                                         |
| `productImage[].exten`                              | string        | jpg                                            |
| `productImage[].size`                               | integer       | 565632                                         |
| `productImage[].src`                                | string        | assets/zuZTCpK0Fng2O6lhdHbou.png               |
| `productKeyword`                                    | array (empty) | array<string>                                  |               |
| `productName`                                       | string        | quick product2                                 |
| `productStage`                                      | object        |                                                |
| `productStage.AdditionalDetails`                    | string        | completed                                      |
| `productStage.PaymentTerms`                         | string        | completed                                      |
| `productStage.PricingAndMoq`                        | string        | completed                                      |
| `productStage.ProductDescription`                   | string        | completed                                      |
| `productStage.ProductInformation`                   | string        | completed                                      |
| `productStage.ProductionAndStock`                   | string        | completed                                      |
| `productStage.ShippingDetails`                      | string        | completed                                      |
| `productStage.Specification`                        | string        | completed                                      |
| `productVideo`                                      | object        |                                                |
| `productVideo.alt`                                  | string        |                                                |
| `productVideo.exten`                                | string        | mp4                                            |
| `productVideo.size`                                 | integer       | 3485909                                        |
| `productVideo.src`                                  | string        |                                                |
| `productionCapacity`                                | object        |                                                |
| `productionCapacity.duration`                       | string        | weekly                                         |
| `productionCapacity.quantity`                       | integer       | 445                                            |
| `productionCapacity.unit`                           | string        | pieces                                         |
| `productionLeadTime`                                | object        |                                                |
| `productionLeadTime.max_day`                        | integer       | 7                                              |
| `productionLeadTime.max_quantity`                   | integer       | 0                                              |
| `productionLeadTime.min_day`                        | integer       | 4                                              |
| `productionLeadTime.min_quantity`                   | integer       | 0                                              |
| `productionLeadTime.unit`                           | string        | unit                                           |
| `samplesAvailability`                               | object        |                                                |
| `samplesAvailability.availabilityType`              | string        | free                                           |
| `samplesAvailability.sampleLeadTime`                | object        |                                                |
| `samplesAvailability.sampleLeadTime.max_day`        | integer       | null                                           | 7             |
| `samplesAvailability.sampleLeadTime.min_day`        | integer       | null                                           | 4             |
| `samplesAvailability.samplePrice`                   | integer       | 10                                             |
| `samplesAvailability.sampleUnit`                    | string        | boxes                                          |
| `shipmentIdentifier`                                | string        | HSN                                            |
| `shippingMethod`                                    | array<string> |                                                |
| `shippingQty`                                       | integer       | 34                                             |
| `shippingUnit`                                      | string        | Pallet                                         |
| `showInCatalog`                                     | boolean       | False                                          |
| `showcase`                                          | boolean       | False                                          |
| `skuCode`                                           | string        | 43256                                          |
| `status`                                            | string        | pending                                        |
| `stockAvailability`                                 | string        | inStock                                        |
| `subCategory`                                       | object        |                                                |
| `subCategory._id`                                   | string        | 67f5154376706f860309ebf0                       |
| `subCategory.name`                                  | string        | Mobile Phones                                  |
| `subCategory.uniqueId`                              | string        | SC9577637767                                   |
| `updatedAt`                                         | date          |                                                |
| `variantAttributes`                                 | array<object> | array (empty)                                  |               |
| `variantAttributes[].key`                           | string        | Brand                                          |
| `variantAttributes[].values`                        | array<string> |                                                |
| `variants`                                          | array<object> | array (empty)                                  |               |
| `variants[]._id`                                    | ObjectId      |                                                |
| `variants[].attributes`                             | object        |                                                |
| `variants[].attributes.Brand`                       | string        | Samsung                                        |
| `variants[].attributes.Color`                       | string        | Red                                            |
| `variants[].attributes.Color Options`               | string        | Black                                          |
| `variants[].attributes.Colour`                      | string        | Red                                            |
| `variants[].attributes.Connectivity`                | string        | Wireless                                       |
| `variants[].attributes.Fabric Type`                 | string        | Silk                                           |
| `variants[].attributes.Flavor`                      | string        | Chocolate Chip                                 |
| `variants[].attributes.Material`                    | string        | Cotton                                         |
| `variants[].attributes.Network Technology`          | string        | 5G                                             |
| `variants[].attributes.Screen Size Range`           | string        | 5 to 6 inches                                  |
| `variants[].attributes.Size`                        | string        | 8                                              |
| `variants[].attributes.color`                       | string        | white                                          |
| `variants[].attributes.gun`                         | string        | air gun                                        |
| `variants[].available`                              | boolean       | True                                           |
| `variants[].isActive`                               | boolean       | True                                           |
| `variants[].isDeleted`                              | boolean       | False                                          |
| `variants[].minOrderQuantity`                       | integer       | 321                                            |
| `variants[].moqUnit`                                | string        | pieces                                         |
| `variants[].pricing`                                | object        |                                                |
| `variants[].pricing.bulkPrices`                     | array<object> |                                                |
| `variants[].pricing.bulkPrices[].maxQty`            | integer       | 200                                            |
| `variants[].pricing.bulkPrices[].minQty`            | integer       | 100                                            |
| `variants[].pricing.bulkPrices[].price`             | integer       | 30000                                          |
| `variants[].pricing.pricingType`                    | string        | fixed                                          |
| `variants[].pricing.unit`                           | string        | pieces                                         |
| `variants[].pricing.unitPrice`                      | integer       | 98                                             |
| `variants[].skuCode`                                | string        | 3432                                           |
| `variants[].variantImg`                             | array<object> | array (empty)                                  | array (empty) | array<object> | array (empty) | array<object> | array (empty) |     |
| `variants[].variantImg[].alt`                       | string        | phone1                                         |
| `variants[].variantImg[].exten`                     | string        | jpeg                                           |
| `variants[].variantImg[].size`                      | integer       | 2508                                           |
| `variants[].variantImg[].src`                       | string        |                                                |
| `variants[].variantName`                            | string        | Samsung / 5 to 6 inches                        |
| `youtubeUrl`                                        | string        |                                                |

### First Document (sanitized)

```json
{
  "_id": "6825afe152a1db8703ef963d",
  "productName": "quick product2",
  "createdBy": "6825afe152a1db8703ef963e",
  "productDescription": "some product description",
  "category": {
    "_id": "67f514ee76706f860309ebe9",
    "name": "Electronics"
  },
  "subCategory": {
    "_id": "67f5154376706f860309ebf0",
    "name": "Mobile Phones"
  },
  "productCategory": {
    "_id": "67f5154376706f860309ebf0",
    "name": "Feature Phones"
  },
  "productImage": [
    {
      "src": "assets/5mp-monochrome-usb-camera_39c4cdec-bbb0-492c-b907-855340dd288e_1744876831439.png",
      "alt": "sdfsdf",
      "exten": "jpg",
      "size": 565632
    },
    {
      "src": "assets/5mp-monochrome-usb-camera_39c4cdec-bbb0-492c-b907-855340dd288e_1744876831439.png",
      "alt": "sdfsdf",
      "exten": "jpg",
      "size": 565632
    }
  ],
  "currency": "USD",
  "pricing": {
    "pricingType": "bulk",
    "unit": "pieces",
    "bulkPrices": [
      {
        "minQty": 1,
        "maxQty": 10,
        "price": 100
      },
      {
        "minQty": 11,
        "maxQty": 50,
        "price": 90
      },
      {
        "minQty": 51,
        "maxQty": 100,
        "price": 80
      }
    ]
  },
  "minOrderQuantity": 10,
  "brandName": "tes brand",
  "isDraft": false,
  "isQuickInsert": true,
  "isArchived": false,
  "showcase": false,
  "productStage": {
    "ProductInformation": "completed",
    "PricingAndMoq": "completed",
    "Specification": "completed",
    "ProductDescription": "completed",
    "ProductionAndStock": "completed",
    "PaymentTerms": "completed",
    "ShippingDetails": "completed",
    "AdditionalDetails": "completed"
  },
  "status": "rejected",
  "createdAt": "2025-05-15T09:12:01.469000",
  "updatedAt": "2025-07-14T10:49:09.623000",
  "__v": 0,
  "liveProductId": "6874e09bce50ecf8d07a97d7",
  "showInCatalog": false
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## selloffers

**Document Count:** 362
**Sample Size:** 100

### Fields

| Field                                   | Type          | Example                                     |
| --------------------------------------- | ------------- | ------------------------------------------- | ------ | ------- | --- |
| `__v`                                   | integer       | 0                                           |
| `_id`                                   | ObjectId      |                                             |
| `assignTo`                              | ObjectId      |                                             |
| `createdAt`                             | date          |                                             |
| `createdBy`                             | ObjectId      |                                             |
| `customPaymentTerm`                     | string        |                                             |
| `dispatchLeadTime`                      | object        |                                             |
| `dispatchLeadTime.max_day`              | integer       | 5                                           |
| `dispatchLeadTime.min_day`              | integer       | 5                                           |
| `immediateStart`                        | boolean       | False                                       |
| `internationalShipping`                 | string        | yes                                         |
| `isArchived`                            | boolean       | False                                       |
| `isDraft`                               | boolean       | False                                       |
| `keyword`                               | array<string> |                                             |
| `marketFocus`                           | array<object> |                                             |
| `marketFocus[].code`                    | string        | BH                                          |
| `marketFocus[].name`                    | string        | Bahrain                                     |
| `offerActive`                           | boolean       | False                                       |
| `offerDescription`                      | string        | based on the order delivery day will change |
| `offerEndDate`                          | date          |                                             |
| `offerId`                               | string        | OFF-93139f2660                              |
| `offerInfo`                             | object        |                                             |
| `offerInfo.buyQty`                      | integer       | 50                                          |
| `offerInfo.currency`                    | string        | object                                      | USD    |
| `offerInfo.currency.code`               | string        | INR                                         |
| `offerInfo.currency.name`               | string        | Indian Rupee                                |
| `offerInfo.currency.symbol`             | string        | ₹                                           |
| `offerInfo.discountPercent`             | integer       | 40                                          |
| `offerInfo.freeQty`                     | integer       | 50                                          |
| `offerInfo.maxQty`                      | integer       | 200                                         |
| `offerInfo.minOrderQuantity`            | integer       | 50                                          |
| `offerInfo.minQty`                      | integer       | 20                                          |
| `offerInfo.offerType`                   | string        | fixedDiscount                               |
| `offerInfo.pricing`                     | object        |                                             |
| `offerInfo.pricing.bulkPrices`          | array<object> |                                             |
| `offerInfo.pricing.bulkPrices[].maxQty` | integer       | 500                                         |
| `offerInfo.pricing.bulkPrices[].minQty` | integer       | 100                                         |
| `offerInfo.pricing.bulkPrices[].price`  | integer       | number                                      | number | integer | 800 |
| `offerInfo.pricing.maxPrice`            | integer       | 1940                                        |
| `offerInfo.pricing.minPrice`            | integer       | 291                                         |
| `offerInfo.pricing.pricingType`         | string        | fixed                                       |
| `offerInfo.pricing.unit`                | string        | boxes                                       |
| `offerInfo.pricing.unitPrice`           | number        | integer                                     | 0.6    |
| `offerInfo.unit`                        | string        | pieces                                      |
| `offerStartDate`                        | date          |                                             |
| `offerTitle`                            | string        | Short time                                  |
| `otherPaymentMethod`                    | string        |                                             |
| `paymentMethods`                        | array<string> |                                             |
| `paymentTerms`                          | array<string> |                                             |
| `postOnFeed`                            | boolean       | False                                       |
| `productId`                             | ObjectId      |                                             |
| `sellOfferStage`                        | object        |                                             |
| `sellOfferStage.OfferDetails`           | string        | completed                                   |
| `sellOfferStage.PaymentShipping`        | string        | completed                                   |
| `sellOfferStage.ProductDetails`         | string        | completed                                   |
| `shippingMethod`                        | array<string> |                                             |
| `showcase`                              | boolean       | False                                       |
| `status`                                | string        | rejected                                    |
| `updatedAt`                             | date          |                                             |

### First Document (sanitized)

```json
{
  "_id": "68257d7ff50d1dac2a58c3eb",
  "productId": "682312e27dbe3d49c950d238",
  "createdBy": "67e2acbbee38d3bc9818a96f",
  "offerActive": false,
  "postOnFeed": false,
  "immediateStart": false,
  "isDraft": true,
  "isArchived": true,
  "showcase": false,
  "sellOfferStage": {
    "ProductDetails": "completed",
    "OfferDetails": "active",
    "PaymentShipping": "pending"
  },
  "createdAt": "2025-05-15T05:37:03.179000",
  "updatedAt": "2025-05-19T11:46:57.169000",
  "__v": 0,
  "dispatchLeadTime": {
    "min_day": 2,
    "max_day": 5
  },
  "internationalShipping": "yes",
  "paymentMethods": ["credit", "paypal", "cash"],
  "paymentTerms": ["ADVANCE_50_DISPATCH_50"],
  "shippingMethod": ["Sea", "Air", "Courier"]
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## sessions

**Document Count:** 4
**Sample Size:** 4

### Fields

| Field       | Type     | Example                  |
| ----------- | -------- | ------------------------ |
| `__v`       | integer  | 0                        |
| `_id`       | ObjectId |                          |
| `createdAt` | date     |                          |
| `hashedRt`  | string   |                          |
| `updatedAt` | date     |                          |
| `user_id`   | string   | 6874d1ddd11244886dd2e76a |

### First Document (sanitized)

```json
{
  "_id": "68761a3d6361980aa68968b4",
  "user_id": "6874d1ddd11244886dd2e76a",
  "hashedRt": "$2a$10$jB9GNS0ofZlJN3jKyMIZceJeO35C2ghRrzyT4Mq6TOfla0mHjWdPC",
  "createdAt": "2025-07-15T09:07:09.449000",
  "updatedAt": "2025-08-06T07:22:30.059000",
  "__v": 0
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## subcategories

**Document Count:** 9
**Sample Size:** 9

### Fields

| Field            | Type          | Example                  |
| ---------------- | ------------- | ------------------------ | --- |
| `_id`            | ObjectId      |                          |
| `annualGrowth`   | string        | 15%                      |
| `averageMargin`  | string        | 30%-40%                  |
| `image`          | string        |                          |
| `liveUrl`        | string        | sports_SC6e16b67695      |
| `mappedChildren` | array (empty) | array<string>            |     |
| `marketSize`     | string        | $250B                    |
| `name`           | string        | sports                   |
| `parentId`       | string        | 67f514f976706f860309ebeb |
| `uniqueId`       | string        | SC6e16b67695             |

### First Document (sanitized)

```json
{
  "_id": "67f5154376706f860309ebf0",
  "uniqueId": "SC9577637767",
  "name": "Mobile Phones",
  "parentId": "67f514ee76706f860309ebe9",
  "mappedChildren": ["6620c91a1f1c8a9a1b1c1001", "67f5124876706f860309ebd0"],
  "liveUrl": "Mobile_Phones_SC9577637767",
  "marketSize": "$250B",
  "annualGrowth": "15%",
  "averageMargin": "30%-40%",
  "image": "assets/mrkt-1_b1a0044d-c978-4bc9-a5a4-2674e89ba7a4_1750222961666.png"
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

**liveUrl_1**

- Type: Unique
- Keys:
  - `liveUrl`: ascending

**uniqueId_1**

- Type: Unique
- Keys:
  - `uniqueId`: ascending

---

## users

**Document Count:** 166
**Sample Size:** 100

### Fields

| Field                                                                | Type          | Example                                 |
| -------------------------------------------------------------------- | ------------- | --------------------------------------- | ------------- |
| `WhatsAppNo`                                                         | object        |                                         |
| `WhatsAppNo.countryCode`                                             | string        | +91                                     |
| `WhatsAppNo.number`                                                  | string        | 8525462222                              |
| `__v`                                                                | integer       | 0                                       |
| `_id`                                                                | ObjectId      |                                         |
| `additionalPhoneNo`                                                  | array (empty) |                                         |
| `assignTo`                                                           | ObjectId      |                                         |
| `businessId`                                                         | ObjectId      |                                         |
| `businessLocation`                                                   | string        | AM                                      |
| `businessType`                                                       | string        | unregister                              |
| `buyerStage`                                                         | object        |                                         |
| `buyerStage.businessDetails`                                         | string        | completed                               |
| `buyerStage.businessOperation`                                       | string        | completed                               |
| `buyerStage.sourcingDetails`                                         | string        | completed                               |
| `countryCode`                                                        | string        | +91                                     |
| `createdAt`                                                          | date          |                                         |
| `currentPlan`                                                        | object        |                                         |
| `currentPlan.autoRenewal`                                            | boolean       | True                                    |
| `currentPlan.billingType`                                            | string        | monthly                                 |
| `currentPlan.endDate`                                                | date          | object                                  |               |
| `currentPlan.endDate.$date`                                          | string        | 2025-07-16T10:59:43.018Z                |
| `currentPlan.isActive`                                               | boolean       | True                                    |
| `currentPlan.isTrial`                                                | boolean       | True                                    |
| `currentPlan.paymentRefId`                                           | string        | 12345                                   |
| `currentPlan.planId`                                                 | string        | P3                                      |
| `currentPlan.startDate`                                              | date          | object                                  |               |
| `currentPlan.startDate.$date`                                        | string        | 2025-07-16T10:59:43.018Z                |
| `dateOfBirth`                                                        | string        | 2025-08-07T18:30:00.000Z                |
| `email`                                                              | string        | test@asd.asd                            |
| `firstName`                                                          | string        | SFgfdgfg                                |
| `isBlocked`                                                          | boolean       | False                                   |
| `isDeleted`                                                          | boolean       | False                                   |
| `isEmailVerified`                                                    | boolean       | False                                   |
| `isPhoneNoVerified`                                                  | boolean       | False                                   |
| `isVerified`                                                         | boolean       | True                                    |
| `jobTitle`                                                           | string        | ddddddddddd                             |
| `lastName`                                                           | string        | dfgfd                                   |
| `middleName`                                                         | string        | weqw                                    |
| `nationalIdNo`                                                       | string        | 789456132222                            |
| `nationalIdType`                                                     | string        | Aadhar                                  |
| `nonprofit`                                                          | object        |                                         |
| `nonprofit.businessOperation`                                        | object        |                                         |
| `nonprofit.businessOperation.businessName`                           | string        |                                         |
| `nonprofit.businessOperation.industry`                               | string        | technology                              |
| `nonprofit.businessOperation.productServiceDescription`              | string        | hjshjshsjhsjhsjhsjhsjhs                 |
| `nonprofit.businessOperation.website`                                | string        |                                         |
| `nonprofit.businessRepresentative`                                   | object        |                                         |
| `nonprofit.businessRepresentative.countryCode`                       | string        | +91                                     |
| `nonprofit.businessRepresentative.dateOfBirth`                       | string        | 1956-05-12                              |
| `nonprofit.businessRepresentative.email`                             | string        | jkjksjdk@ksjdksj.com                    |
| `nonprofit.businessRepresentative.homeAddress`                       | object        |                                         |
| `nonprofit.businessRepresentative.homeAddress.apartmentUnitOrOther`  | string        | 1212                                    |
| `nonprofit.businessRepresentative.homeAddress.cityTown`              | string        | Erode                                   |
| `nonprofit.businessRepresentative.homeAddress.country`               | string        | IN                                      |
| `nonprofit.businessRepresentative.homeAddress.postalCode`            | string        | 638107                                  |
| `nonprofit.businessRepresentative.homeAddress.streetAddress`         | string        | Strresd                                 |
| `nonprofit.businessRepresentative.jobTitle`                          | string        | kjsdkjksdj`                             |
| `nonprofit.businessRepresentative.name`                              | string        | John                                    |
| `nonprofit.businessRepresentative.personalIdNo`                      | number        | 5454545754545454.0                      |
| `nonprofit.businessRepresentative.phoneNo`                           | string        | 8610849174                              |
| `nonprofit.complianceDetail`                                         | object        |                                         |
| `nonprofit.complianceDetail.VATNumber`                               | string        |                                         |
| `nonprofit.complianceDetail.businessName`                            | string        | ABC                                     |
| `nonprofit.complianceDetail.companyRegisterNumber`                   | integer       | number                                  | 123456789     |
| `nonprofit.contactInformation`                                       | object        |                                         |
| `nonprofit.contactInformation.businessAddress`                       | object        |                                         |
| `nonprofit.contactInformation.businessAddress.apartmentUnitOrOther`  | string        | 5656                                    |
| `nonprofit.contactInformation.businessAddress.cityTown`              | string        | Erode                                   |
| `nonprofit.contactInformation.businessAddress.country`               | string        | IN                                      |
| `nonprofit.contactInformation.businessAddress.postalCode`            | string        | 638107                                  |
| `nonprofit.contactInformation.businessAddress.streetAddress`         | string        | 456                                     |
| `nonprofit.contactInformation.email`                                 | string        | abc@gmail.com                           |
| `nonprofit.contactInformation.phoneNo`                               | string        | 9876433100                              |
| `nonprofit.contactInformation.productServiceDescription`             | string        | spdlspdlspdlsds                         |
| `notificationPreferences`                                            | object        |                                         |
| `notificationPreferences.dealAlerts`                                 | object        |                                         |
| `notificationPreferences.dealAlerts.email`                           | boolean       | True                                    |
| `notificationPreferences.dealAlerts.mobile`                          | boolean       | True                                    |
| `notificationPreferences.featureUpdate`                              | object        |                                         |
| `notificationPreferences.featureUpdate.email`                        | boolean       | False                                   |
| `notificationPreferences.featureUpdate.mobile`                       | boolean       | False                                   |
| `notificationPreferences.followUp`                                   | object        |                                         |
| `notificationPreferences.followUp.email`                             | boolean       | True                                    |
| `notificationPreferences.followUp.mobile`                            | boolean       | True                                    |
| `notificationPreferences.insights`                                   | object        |                                         |
| `notificationPreferences.insights.email`                             | boolean       | False                                   |
| `notificationPreferences.insights.mobile`                            | boolean       | False                                   |
| `notificationPreferences.message`                                    | object        |                                         |
| `notificationPreferences.message.email`                              | boolean       | True                                    |
| `notificationPreferences.message.mobile`                             | boolean       | True                                    |
| `notificationPreferences.productUpdates`                             | object        |                                         |
| `notificationPreferences.productUpdates.email`                       | boolean       | False                                   |
| `notificationPreferences.productUpdates.mobile`                      | boolean       | False                                   |
| `notificationPreferences.promotions`                                 | object        |                                         |
| `notificationPreferences.promotions.email`                           | boolean       | False                                   |
| `notificationPreferences.promotions.mobile`                          | boolean       | False                                   |
| `onBoardingComplete`                                                 | boolean       | False                                   |
| `onBoardingSkipped`                                                  | boolean       | False                                   |
| `personalAddress`                                                    | object        |                                         |
| `personalAddress.addressLine`                                        | string        | dfdfdfdf                                |
| `personalAddress.city`                                               | string        | Ashkāsham                               |
| `personalAddress.country`                                            | object        |                                         |
| `personalAddress.country.code`                                       | string        | AF                                      |
| `personalAddress.country.name`                                       | string        | Afghanistan                             |
| `personalAddress.pincode`                                            | string        | 44444                                   |
| `personalAddress.state`                                              | string        | Badakhshan                              |
| `phoneNo`                                                            | string        | 9596565656                              |
| `profilePic`                                                         | string        |                                         |
| `register`                                                           | object        |                                         |
| `register.businessOperation`                                         | object        |                                         |
| `register.businessOperation.businessName`                            | string        | New business                            |
| `register.businessOperation.industry`                                | string        | manufacturing                           |
| `register.businessOperation.productServiceDescription`               | string        | sdfsdf                                  |
| `register.businessOperation.website`                                 | string        | www.sktech.com                          |
| `register.businessRepresentative`                                    | object        |                                         |
| `register.businessRepresentative.countryCode`                        | string        | +91                                     |
| `register.businessRepresentative.dateOfBirth`                        | string        | 2025-07-10                              |
| `register.businessRepresentative.email`                              | string        | lafofej180@dxirl.com                    |
| `register.businessRepresentative.homeAddress`                        | object        |                                         |
| `register.businessRepresentative.homeAddress.apartmentUnitOrOther`   | string        | fvv                                     |
| `register.businessRepresentative.homeAddress.cityTown`               | string        | erode                                   |
| `register.businessRepresentative.homeAddress.country`                | string        | IN                                      |
| `register.businessRepresentative.homeAddress.postalCode`             | string        | 600001                                  |
| `register.businessRepresentative.homeAddress.streetAddress`          | string        | fff                                     |
| `register.businessRepresentative.jobTitle`                           | string        | saler                                   |
| `register.businessRepresentative.name`                               | string        | Arjun sharma                            |
| `register.businessRepresentative.personalIdNo`                       | integer       | number                                  | 567           |
| `register.businessRepresentative.phoneNo`                            | string        | 8754817769                              |
| `register.complianceDetail`                                          | object        |                                         |
| `register.complianceDetail.VATNumber`                                | string        | dgdfg                                   |
| `register.complianceDetail.businessName`                             | string        | sdfsdf                                  |
| `register.complianceDetail.companyRegisterNumber`                    | integer       | number                                  | 3245345       |
| `register.complienceDetails`                                         | object        |                                         |
| `register.contactInformation`                                        | object        |                                         |
| `register.contactInformation.businessAddress`                        | object        |                                         |
| `register.contactInformation.businessAddress.apartmentUnitOrOther`   | string        | sdfsdfsfs                               |
| `register.contactInformation.businessAddress.cityTown`               | string        | Saint David’s                           |
| `register.contactInformation.businessAddress.country`                | string        | GD                                      |
| `register.contactInformation.businessAddress.postalCode`             | string        | 4000014                                 |
| `register.contactInformation.businessAddress.streetAddress`          | string        | 456, XYZ Road                           |
| `register.contactInformation.email`                                  | string        | antoraphael02@gmail.com                 |
| `register.contactInformation.phoneNo`                                | string        | 09600976566                             |
| `register.contactInformation.productServiceDescription`              | string        | sdfsdfsdf                               |
| `registerStatus`                                                     | object        |                                         |
| `registerStatus.businessDetails`                                     | string        | completed                               |
| `registerStatus.businessOperation`                                   | string        | completed                               |
| `registerStatus.businessRepresentative`                              | string        | active                                  |
| `registerStatus.contactInformation`                                  | string        | completed                               |
| `registerStatus.personalInformation`                                 | string        | completed                               |
| `source`                                                             | string        | Pepagora Signup Page                    |
| `status`                                                             | string        | rejected                                |
| `unRegisterStatus`                                                   | object        |                                         |
| `unRegisterStatus.businessDetails`                                   | string        | completed                               |
| `unRegisterStatus.businessOperation`                                 | string        | completed                               |
| `unRegisterStatus.businessRepresentative`                            | string        | completed                               |
| `unRegisterStatus.personalInformation`                               | string        | active                                  |
| `unregister`                                                         | object        |                                         |
| `unregister.businessOperation`                                       | object        |                                         |
| `unregister.businessOperation.businessName`                          | string        | sdfsdf                                  |
| `unregister.businessOperation.industry`                              | string        | technology                              |
| `unregister.businessOperation.productServiceDescription`             | string        | sdfsdfsdfsdf                            |
| `unregister.businessOperation.website`                               | string        |                                         |
| `unregister.contactInformation`                                      | object        |                                         |
| `unregister.contactInformation.businessAddress`                      | object        |                                         |
| `unregister.contactInformation.businessAddress.apartmentUnitOrOther` | string        | Puliyakulam Road, Pappanaicken Palayem, |
| `unregister.contactInformation.businessAddress.cityTown`             | string        | Coimbatore                              |
| `unregister.contactInformation.businessAddress.country`              | string        | IN                                      |
| `unregister.contactInformation.businessAddress.postalCode`           | string        | 641037                                  |
| `unregister.contactInformation.businessAddress.streetAddress`        | string        | #59/2, T2, Soundarya Regency            |
| `unregister.contactInformation.email`                                | string        | deepak.s@pepagora.com                   |
| `unregister.contactInformation.phoneNo`                              | string        | 6362169984                              |
| `unregister.contactInformation.productServiceDescription`            | string        | we sell hardware components             |
| `unregister.personalInformation`                                     | object        |                                         |
| `unregister.personalInformation.dateOfBirth`                         | string        | 2024-12-27                              |
| `unregister.personalInformation.email`                               | string        | testuser9999@gmail.com                  |
| `unregister.personalInformation.name`                                | string        | UAT changes                             |
| `unregister.personalInformation.personalIdNo`                        | number        | integer                                 | 34234234234.0 |
| `updatedAt`                                                          | date          |                                         |
| `userType`                                                           | string        | buyer                                   |
| `workEmail`                                                          | string        | wqeqwe@gmail.com                        |
| `workPhoneNo`                                                        | object        |                                         |
| `workPhoneNo.countryCode`                                            | string        | +91                                     |
| `workPhoneNo.number`                                                 | string        | 8525462222                              |

### First Document (sanitized)

```json
{
  "_id": "685b83c9640c0efe0929cfa6",
  "email": "gobikasekar@solutionchamps.com",
  "isEmailVerified": false,
  "phoneNo": "8220041817",
  "countryCode": "+91",
  "isPhoneNoVerified": false,
  "isVerified": true,
  "isDeleted": false,
  "isBlocked": false,
  "onBoardingComplete": true,
  "onBoardingSkipped": false,
  "createdAt": "2025-07-11T07:14:10.054000",
  "updatedAt": "2025-08-09T14:11:49.032000",
  "__v": 0,
  "userType": "both",
  "businessLocation": "DZ",
  "businessType": "register",
  "register": {
    "complianceDetail": {
      "businessName": "xxxxxx",
      "companyRegisterNumber": 23243534,
      "VATNumber": "dfdg"
    },
    "businessOperation": {
      "businessName": "abc limited",
      "industry": "manufacturing",
      "website": "gobika.com",
      "productServiceDescription": "testttt"
    },
    "contactInformation": {
      "phoneNo": "8220041817",
      "email": "gobikasekar@solutionchamps.com",
      "businessAddress": {
        "country": "BH",
        "streetAddress": "asas",
        "apartmentUnitOrOther": "232",
        "cityTown": "Manama",
        "postalCode": "110019"
      },
      "productServiceDescription": "testeddddddddd"
    },
    "businessRepresentative": {
      "name": "Gobika",
      "email": "gobikasekar@solutionchamps.com",
      "jobTitle": "Ceo",
      "dateOfBirth": "2025-06-27",
      "homeAddress": {
        "country": "IS",
        "streetAddress": "ghj",
        "apartmentUnitOrOther": "ghgj",
        "cityTown": "'ghgj",
        "postalCode": "53434"
      },
      "personalIdNo": 1323435456,
      "phoneNo": "8220041817",
      "countryCode": "+91"
    }
  },
  "status": "pending",
  "source": "Pepagora Signup Page",
  "currentPlan": {
    "planId": "P5",
    "billingType": "monthly",
    "startDate": "2025-07-16T10:59:43.018000",
    "endDate": "2025-07-16T10:59:43.018000",
    "isActive": true,
    "isTrial": true,
    "paymentRefId": "12345",
    "autoRenewal": true
  },
  "jobTitle": "CTO DD",
  "assignTo": "6874d1ddd11244886dd2e764",
  "additionalPhoneNo": [],
  "notificationPreferences": {
    "message": {
      "email": true,
      "mobile": true
    },
    "followUp": {
      "email": false,
      "mobile": false
    },
    "dealAlerts": {
      "email": true,
      "mobile": false
    },
    "featureUpdate": {
      "email": true,
      "mobile": true
    },
    "productUpdates": {
      "email": false,
      "mobile": false
    },
    "promotions": {
      "email": false,
      "mobile": false
    },
    "insights": {
      "email": false,
      "mobile": false
    }
  }
}
```

### Indexes

**_id_**

- Keys:
  - `_id`: ascending

---

## Generation Info

- **MongoDB URI:** `URI`
- **Sample Size per Collection:** 100
- **Generated by:** MongoDB Schema Extractor
