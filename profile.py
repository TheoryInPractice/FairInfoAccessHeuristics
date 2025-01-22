# Import the Portal object.
import geni.portal as portal
import geni.rspec.pg as rspec

# Create a Request object to start building the RSpec.
request = portal.context.makeRequestRSpec()
 
# Add a XenVM (named "node") to the request
node = request.XenVM("node")

# Write the request in RSpec format
portal.context.printRequestRSpec()
