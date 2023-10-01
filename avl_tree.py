class TreeNode(object):
	def __init__(self, val, content):
		self.val = val
		self.content = content
		self.left = None
		self.right = None
		self.height = 1

class Proyect(object):
	def __init__(self):
		self.id = ""
		self.nombre = ""
		self.prioridad = ""
		pass

class AVL_Tree(object):

	def insert(self, root, key, content):
		# Step 1 - Perform normal BST
		if not root:
			return TreeNode(key, content)
		elif key < root.val:
			root.left = self.insert(root.left, key, content)
		else:
			root.right = self.insert(root.right, key, content)

		# Step 2 - Update the height of the
		# ancestor node
		root.height = 1 + max(self.getHeight(root.left),
						self.getHeight(root.right))

		# Step 3 - Get the balance factor
		balance = self.getBalance(root)

		# Step 4 - If the node is unbalanced,
		# then try out the 4 cases
		# Case 1 - Left Left
		if balance > 1 and key < root.left.val:
			return self.rightRotate(root)

		# Case 2 - Right Right
		if balance < -1 and key > root.right.val:
			return self.leftRotate(root)

		# Case 3 - Left Right
		if balance > 1 and key > root.left.val:
			root.left = self.leftRotate(root.left)
			return self.rightRotate(root)

		# Case 4 - Right Left
		if balance < -1 and key < root.right.val:
			root.right = self.rightRotate(root.right)
			return self.leftRotate(root)

		return root

	def leftRotate(self, z):

		y = z.right
		T2 = y.left

		# Perform rotation
		y.left = z
		z.right = T2

		# Update heights
		z.height = 1 + max(self.getHeight(z.left),
						self.getHeight(z.right))
		y.height = 1 + max(self.getHeight(y.left),
						self.getHeight(y.right))

		# Return the new root
		return y

	def rightRotate(self, z):

		y = z.left
		T3 = y.right

		# Perform rotation
		y.right = z
		z.left = T3

		# Update heights
		z.height = 1 + max(self.getHeight(z.left),
						self.getHeight(z.right))
		y.height = 1 + max(self.getHeight(y.left),
						self.getHeight(y.right))

		# Return the new root
		return y

	def getHeight(self, root):
		if not root:
			return 0

		return root.height

	def getBalance(self, root):
		if not root:
			return 0

		return self.getHeight(root.left) - self.getHeight(root.right)

	def preOrder(self, root):

		if not root:
			return

		print("{0} ".format(root.val), end="")
		self.preOrder(root.left)
		self.preOrder(root.right)

	def delete(self, root, key):
	
		# Step 1 - Perform standard BST delete
		if not root:
			return root
	
		elif key < root.val:
			root.left = self.delete(root.left, key)
	
		elif key > root.val:
			root.right = self.delete(root.right, key)
	
		else:
			if root.left is None:
				temp = root.right
				root = None
				return temp
			
	def search(self, root, key):
		if root == None:
			return None
		elif root.val == key:
			return root
		elif root.val > key:
			return self.search(root.left, key)
		else:
			return self.search(root.right, key)