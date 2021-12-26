class BaseTool:
    def error(self, message):
        return { 'status': 'error', 'error': message }

    def success(self, results, progress=0):
        if progress > 0:
            return { 'status': 'success', 'results': results, 'progress': progress }
        else:
            return { 'status': 'success', 'results': results }
